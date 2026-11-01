from app.llm.client import llm_client
from app.llm.parser import LLMParser
from app.registry.competency_registry import (
    competency_registry,
)


class CompetencyAnalyzer:

    # ==================================================
    # REGISTRY
    # ==================================================

    def _get_competencies(self) -> list[dict]:

        if hasattr(competency_registry, "competencies"):
            entries = competency_registry.competencies

        elif hasattr(competency_registry, "_competencies"):
            entries = competency_registry._competencies

        elif hasattr(competency_registry, "items"):
            entries = [
                entry
                for _, entry in competency_registry.items()
            ]

        else:
            raise AttributeError(
                "Unable to access competency registry."
            )

        if isinstance(entries, dict):
            entries = entries.values()

        result = []

        for competency in entries:

            if hasattr(competency, "model_dump"):
                data = competency.model_dump(
                    mode="json"
                )
            else:
                data = vars(competency)

            result.append(
                {
                    "id": data.get(
                        "id",
                        getattr(
                            competency,
                            "id",
                            "",
                        ),
                    ),
                    "name": data.get(
                        "name",
                        getattr(
                            competency,
                            "name",
                            "",
                        ),
                    ),
                    "description": data.get(
                        "description",
                        getattr(
                            competency,
                            "description",
                            "",
                        ),
                    ),
                    "questions": data.get(
                        "questions",
                        getattr(
                            competency,
                            "questions",
                            [],
                        ),
                    ),
                }
            )

        return result

    # ==================================================
    # SINGLE-PASS MAPPING
    # ==================================================

    def _build_mapping_prompt(
        self,
        competencies: list[dict],
        behavioral_atoms: list[dict],
    ) -> str:

        competency_text = "\n\n".join(
            (
                f"ID: {competency['id']}\n"
                f"NAME: {competency['name']}\n"
                f"DEFINITION: {competency['description']}"
            )
            for competency in competencies
        )

        evidence_text = "\n\n".join(
            (
                f"ATOM {atom['id']}\n"
                f"Time: "
                f"{atom.get('source_start', '')} - "
                f"{atom.get('source_end', '')}\n"
                f"Behavior: "
                f"{atom.get('behavior', '')}\n"
                f"Decision / Reasoning: "
                f"{atom.get('decision_reasoning', '')}\n"
                f"Result: "
                f"{atom.get('result', '')}\n"
                f"Quote: "
                f"{atom.get('quote', '')}"
            )
            for atom in behavioral_atoms
        )

        return f"""
You are an expert behavioral interview evidence-mapping engine.

Your task is to map behavioral evidence atoms to the
competencies they genuinely demonstrate.

You are evaluating ALL competencies simultaneously.

Do NOT score competencies.

Do NOT invent behavior.

Do NOT infer behavior that is absent.

An evidence atom may support multiple competencies.

Only map an atom when the actual behavior provides
meaningful evidence for that competency.

Do not map an atom simply because:
- the competency name appears conceptually related
- the candidate achieved a successful result
- the behavior is generic
- the competency could theoretically be involved

Judge the actual behavior described.

Examples:

If the candidate says they worked closely with
consumer insights, marketing, product and finance,
this can support teamwork.

If the candidate describes building rapport with
stakeholders and using market trends, competitor
examples and analytics to persuade them, this can
support influencing_others and interpersonal_skills.

If the candidate describes developing new positioning,
messaging or a novel marketing strategy, this may
support creativity.

If the candidate describes selecting an approach,
testing alternatives or changing strategy based on
evidence, this may support decision_making.

Do not require the candidate to explicitly use the
competency terminology.

Do not reward business outcomes by themselves.

Every mapping must contain:
- atom_id
- competency_id
- strength
- reason

Strength levels:

weak
moderate
strong
exceptional

weak = limited but relevant evidence

moderate = clear behavioral evidence

strong = specific and convincing behavioral evidence

exceptional = unusually strong, specific and repeated
behavioral evidence

Return ONLY valid JSON.

COMPETENCIES:

{competency_text}

BEHAVIORAL EVIDENCE:

{evidence_text}

FORMAT:

{{
  "mappings": [
    {{
      "atom_id": "A001",
      "competency_id": "decision_making",
      "strength": "strong",
      "reason": "The candidate used performance data to select an approach."
    }}
  ]
}}

If no mappings exist:

{{
  "mappings": []
}}
"""

    # ==================================================
    # SINGLE MAPPING CALL
    # ==================================================

    def _map_all_competencies(
        self,
        competencies: list[dict],
        behavioral_atoms: list[dict],
    ) -> list[dict]:

        prompt = self._build_mapping_prompt(
            competencies,
            behavioral_atoms,
        )

        print(
            "[COMPETENCY] Mapping all evidence "
            "in a single LLM call..."
        )

        raw = llm_client.generate_json(
            prompt=prompt,
            schema={
                "type": "object",
                "properties": {
                    "mappings": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "atom_id": {
                                    "type": "string"
                                },
                                "competency_id": {
                                    "type": "string"
                                },
                                "strength": {
                                    "type": "string",
                                    "enum": [
                                        "weak",
                                        "moderate",
                                        "strong",
                                        "exceptional",
                                    ],
                                },
                                "reason": {
                                    "type": "string"
                                },
                            },
                            "required": [
                                "atom_id",
                                "competency_id",
                                "strength",
                                "reason",
                            ],
                        },
                    }
                },
                "required": [
                    "mappings"
                ],
            },
        )

        data = LLMParser.parse_json(raw)

        mappings = data.get(
            "mappings",
            [],
        )

        print(
            "[COMPETENCY] Evidence mappings: "
            f"{len(mappings)}"
        )

        return mappings

    # ==================================================
    # SINGLE-PASS SCORING
    # ==================================================

    def _build_scoring_prompt(
        self,
        competencies: list[dict],
        grouped_evidence: dict,
    ) -> str:

        competency_sections = []

        for competency in competencies:

            competency_id = competency["id"]

            supporting = grouped_evidence.get(
                competency_id,
                [],
            )

            evidence_text = "\n".join(
                (
                    f"- Atom {item['atom_id']}\n"
                    f"  Strength: {item['strength']}\n"
                    f"  Mapping reason: {item['reason']}\n"
                    f"  Behavior: {item['atom']['behavior']}\n"
                    f"  Reasoning: {item['atom']['decision_reasoning']}\n"
                    f"  Result: {item['atom']['result']}\n"
                    f"  Quote: {item['atom']['quote']}"
                )
                for item in supporting
            )

            if not evidence_text:
                evidence_text = "NO DIRECT EVIDENCE"

            competency_sections.append(
                (
                    f"COMPETENCY: {competency_id}\n"
                    f"NAME: {competency['name']}\n"
                    f"DEFINITION: {competency['description']}\n"
                    f"EVIDENCE:\n{evidence_text}"
                )
            )

        competency_text = "\n\n".join(
            competency_sections
        )

        return f"""
You are an expert behavioral interview assessor.

Assess ALL competencies below.

Use ONLY the supplied behavioral evidence.

Do not invent evidence.

Do not reward business outcomes by themselves.

Do not count duplicate transcript fragments as
separate examples.

Judge behavioral quality, specificity and consistency.

If there is no meaningful direct behavioral evidence
for a competency, set:

"rating": null
"confidence": 0
"assessment_status": "insufficient_evidence"

Do NOT give a low numerical score simply because
evidence is absent.

RATING SCALE:

1 = CONTRARY
Evidence demonstrates behavior contrary to the
competency.

2 = LIMITED
Some relevant evidence exists, but demonstration is
weak or incomplete.

3 = SUFFICIENT
Clear evidence adequately demonstrates the competency.

4 = STRONG
Multiple specific examples demonstrate the competency
consistently.

5 = ROLE_MODEL
Exceptional and repeated evidence demonstrates behavior
that could serve as a role model.

Return ONLY valid JSON.

COMPETENCIES AND EVIDENCE:

{competency_text}

FORMAT:

{{
  "competencies": [
    {{
      "competency_id": "decision_making",
      "rating": 3,
      "confidence": 0.82,
      "assessment_status": "assessed",
      "rationale": "The candidate demonstrated..."
    }},
    {{
      "competency_id": "teamwork",
      "rating": null,
      "confidence": 0,
      "assessment_status": "insufficient_evidence",
      "rationale": "The interview did not provide sufficient direct evidence."
    }}
  ]
}}
"""

    # ==================================================
    # SINGLE SCORING CALL
    # ==================================================

    def _score_all_competencies(
        self,
        competencies: list[dict],
        grouped_evidence: dict,
    ) -> list[dict]:

        prompt = self._build_scoring_prompt(
            competencies,
            grouped_evidence,
        )

        print(
            "[COMPETENCY] Scoring all competencies "
            "in a single LLM call..."
        )

        raw = llm_client.generate_json(
            prompt=prompt,
            schema={
                "type": "object",
                "properties": {
                    "competencies": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "competency_id": {
                                    "type": "string"
                                },
                                "rating": {
                                    "type": [
                                        "integer",
                                        "null"
                                    ],
                                    "minimum": 1,
                                    "maximum": 5,
                                },
                                "confidence": {
                                    "type": "number",
                                    "minimum": 0,
                                    "maximum": 1,
                                },
                                "assessment_status": {
                                    "type": "string",
                                    "enum": [
                                        "assessed",
                                        "insufficient_evidence",
                                    ],
                                },
                                "rationale": {
                                    "type": "string"
                                },
                            },
                            "required": [
                                "competency_id",
                                "rating",
                                "confidence",
                                "assessment_status",
                                "rationale",
                            ],
                        },
                    }
                },
                "required": [
                    "competencies"
                ],
            },
        )

        data = LLMParser.parse_json(raw)

        return data.get(
            "competencies",
            [],
        )

    # ==================================================
    # PUBLIC API
    # ==================================================

    def analyze(
        self,
        behavioral_atoms: list[dict],
    ) -> dict:

        if not behavioral_atoms:
            raise ValueError(
                "No behavioral atoms available."
            )

        competencies = self._get_competencies()

        print(
            "[COMPETENCY] Mapping evidence..."
        )

        all_mappings = self._map_all_competencies(
            competencies,
            behavioral_atoms,
        )

        atom_lookup = {
            atom["id"]: atom
            for atom in behavioral_atoms
        }

        competency_lookup = {
            competency["id"]: competency
            for competency in competencies
        }

        grouped = {
            competency["id"]: []
            for competency in competencies
        }

        valid_mappings = []
        seen = set()

        # ==================================================
        # VALIDATE MAPPINGS
        # ==================================================

        for mapping in all_mappings:

            atom_id = mapping.get(
                "atom_id"
            )

            competency_id = mapping.get(
                "competency_id"
            )

            if atom_id not in atom_lookup:
                continue

            if competency_id not in competency_lookup:
                continue

            key = (
                atom_id,
                competency_id,
            )

            if key in seen:
                continue

            seen.add(key)

            atom = atom_lookup[
                atom_id
            ]

            evidence_item = {
                "atom_id": atom_id,
                "strength": mapping.get(
                    "strength",
                    "weak",
                ),
                "reason": mapping.get(
                    "reason",
                    "",
                ),
                "atom": atom,
            }

            grouped[
                competency_id
            ].append(
                evidence_item
            )

            valid_mappings.append(
                mapping
            )

        print(
            "[COMPETENCY] Valid evidence mappings: "
            f"{len(valid_mappings)}"
        )

        # ==================================================
        # SCORE
        # ==================================================

        print(
            "[COMPETENCY] Scoring "
            f"{len(competencies)} competencies..."
        )

        raw_results = self._score_all_competencies(
            competencies,
            grouped,
        )

        result_lookup = {
            result.get("competency_id"): result
            for result in raw_results
        }

        results = []

        # ==================================================
        # NORMALIZE RESULTS
        # ==================================================

        for competency in competencies:

            competency_id = competency["id"]

            supporting = grouped.get(
                competency_id,
                [],
            )

            score = result_lookup.get(
                competency_id
            )

            # ----------------------------------------------
            # Missing result from LLM
            # ----------------------------------------------

            if score is None:

                result = {
                    "competency_id":
                        competency_id,
                    "rating": None,
                    "confidence": 0,
                    "supporting_evidence": [
                        item["atom_id"]
                        for item in supporting
                    ],
                    "evidence_strength": (
                        "none"
                        if not supporting
                        else "unknown"
                    ),
                    "assessment_status":
                        "insufficient_evidence",
                    "rationale": (
                        "The model did not return "
                        "a valid assessment."
                    ),
                }

                results.append(result)
                continue

            # ----------------------------------------------
            # Evidence strength
            # ----------------------------------------------

            strengths = {
                item["strength"]
                for item in supporting
            }

            if "exceptional" in strengths:
                overall_strength = "exceptional"

            elif "strong" in strengths:
                overall_strength = "strong"

            elif "moderate" in strengths:
                overall_strength = "moderate"

            elif "weak" in strengths:
                overall_strength = "weak"

            else:
                overall_strength = "none"

            # ----------------------------------------------
            # Normalize rating
            # ----------------------------------------------

            rating = score.get(
                "rating"
            )

            if rating is not None:

                rating = max(
                    1,
                    min(
                        5,
                        int(rating),
                    ),
                )

            confidence = max(
                0.0,
                min(
                    1.0,
                    float(
                        score.get(
                            "confidence",
                            0,
                        )
                    ),
                ),
            )

            assessment_status = score.get(
                "assessment_status",
                (
                    "assessed"
                    if rating is not None
                    else "insufficient_evidence"
                ),
            )

            result = {
                "competency_id":
                    competency_id,
                "rating":
                    rating,
                "confidence":
                    confidence,
                "supporting_evidence": [
                    item["atom_id"]
                    for item in supporting
                ],
                "evidence_strength":
                    overall_strength,
                "assessment_status":
                    assessment_status,
                "rationale":
                    str(
                        score.get(
                            "rationale",
                            "",
                        )
                    ),
            }

            results.append(result)

        # ==================================================
        # RETURN
        # ==================================================

        return {
            "competencies": results,
            "evidence_mappings": valid_mappings,
        }


competency_analyzer = CompetencyAnalyzer()