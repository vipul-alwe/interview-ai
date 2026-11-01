from app.domain.evidence import Evidence, EvidencePolarity
from app.domain.response import Response
from app.llm.client import llm_client
from app.llm.parser import LLMParser
from app.registry.competency_registry import competency_registry


class EvidenceExtractor:

    def _build_prompt(
        self,
        response: Response,
    ) -> str:

        competencies = []

        for competency in competency_registry.all():

            competencies.append(
                f"""
ID: {competency.id}
NAME: {competency.name}
DESCRIPTION: {competency.description}
""".strip()
            )

        competency_text = "\n\n".join(
            competencies
        )

        return f"""
You are a behavioral interview evidence extraction engine.

Your task is to analyze the candidate's response and
extract ONLY evidence that is directly supported by the
candidate's words.

Do not score the candidate.

Do not infer personality.

Do not make hiring recommendations.

An individual piece of evidence may support multiple
competencies.

Only assign a competency when the transcript provides
direct behavioral evidence relevant to that competency.

COMPETENCIES

{competency_text}

QUESTION

{response.question_id}

CANDIDATE RESPONSE

{response.transcript}

Return ONLY valid JSON in this exact structure:

{{
  "evidence": [
    {{
      "competency_id": "one_of_the_ids_above",
      "quote": "exact quote from candidate",
      "reasoning": "why this quote is evidence for the competency",
      "polarity": "positive",
      "confidence": 0.0
    }}
  ]
}}

Rules:

- competency_id must exactly match one of the competency IDs.
- quote must be directly supported by the transcript.
- Do not invent facts.
- Do not duplicate identical evidence.
- confidence must be between 0.0 and 1.0.
- polarity must be one of:
  positive, negative, neutral.
- Return an empty evidence array if there is no meaningful evidence.
"""

    async def extract(
        self,
        response: Response,
    ) -> list[Evidence]:

        prompt = self._build_prompt(
            response
        )

        raw_output = llm_client.generate(
            prompt
        )

        data = LLMParser.parse_json(
            raw_output
        )

        if not isinstance(data, dict):
            raise ValueError(
                "Evidence extractor returned "
                "an invalid JSON structure."
            )

        items = data.get(
            "evidence",
            []
        )

        if not isinstance(items, list):
            raise ValueError(
                "'evidence' must be a list."
            )

        valid_competencies = {
            competency.id
            for competency in competency_registry.all()
        }

        extracted = []

        for item in items:

            competency_id = item.get(
                "competency_id"
            )

            if competency_id not in valid_competencies:
                continue

            extracted.append(
                Evidence(
                    competency_id=competency_id,
                    quote=item["quote"],
                    reasoning=item["reasoning"],
                    polarity=EvidencePolarity(
                        item["polarity"]
                    ),
                    confidence=float(
                        item["confidence"]
                    ),
                    question_id=response.question_id,
                )
            )

        return extracted


evidence_extractor = EvidenceExtractor()