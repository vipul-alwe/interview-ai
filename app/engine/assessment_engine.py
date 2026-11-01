from app.domain.competency_state import CompetencyState
from app.domain.evidence_assessment import (
    EvidenceAssessment,
    EvidenceRating,
)
from app.llm.client import llm_client
from app.llm.parser import LLMParser
from app.registry.competency_registry import (
    competency_registry,
)


class AssessmentEngine:

    def _build_prompt(
        self,
        competency_id: str,
        state: CompetencyState,
    ) -> str:

        competency = competency_registry.get(
            competency_id
        )

        evidence_text = "\n\n".join(
            f"""
Evidence {index}:

Quote:
{item.quote}

Evidence reasoning:
{item.reasoning}

Polarity:
{item.polarity.value}

Confidence:
{item.confidence}
""".strip()
            for index, item in enumerate(
                state.evidence,
                start=1,
            )
        )

        questions = "\n".join(
            f"- {question}"
            for question in competency.questions
        )

        return f"""
You are a behavioral interview assessment engine.

Assess ONLY the competency provided below.

COMPETENCY

ID: {competency.id}
Name: {competency.name}

Definition:
{competency.description}

Behavioral interview questions from the competency framework:

{questions}

EVIDENCE

{evidence_text}

ASSESSMENT

Assess how strongly the evidence demonstrates the
competency according to the definition above.

Rating scale:

1 = CONTRARY
2 = INSUFFICIENT
3 = SUFFICIENT
4 = NUMEROUS
5 = ROLE_MODEL

Interpretation:

1:
Evidence contradicts or demonstrates poor behavior
related to the competency.

2:
Some relevant evidence exists, but it is insufficient
to establish the competency reliably.

3:
The evidence demonstrates the competency adequately.

4:
There is strong, specific, and repeated evidence of
the competency.

5:
The evidence demonstrates exceptional, highly
effective behavior that could serve as a role model.

IMPORTANT RATING RULES:

- Judge the evidence against the competency definition.
- Do not reward evidence merely because it sounds positive.
- Do not infer behaviors that are not present.
- A single narrow example should normally not receive 4 or 5.
- Distinguish taking ownership from demonstrating the
  complete competency.
- Do not invent missing evidence.
- Confidence must be between 0.0 and 1.0.

RATIONALE REQUIREMENTS:

The rationale must explain the rating using the
candidate's ACTUAL evidence.

The evidence QUOTE is the primary source of truth.

The rationale MUST:

- Describe what the candidate actually did.
- Use specific actions from the evidence.
- Preserve concrete details from the evidence whenever
  available, including numbers, durations, timelines,
  sequence of actions, stakeholders, tools, requirements,
  and outcomes.
- Explain why those specific actions support the competency.
- Be specific to this candidate and this interview.
- Stay grounded entirely in the supplied evidence.
- Never invent facts, outcomes, responsibilities, or
  behaviors.
- Never substitute generic competency language for the
  candidate's actual behavior.

DO NOT write generic rationales such as:

"The candidate demonstrated strong ability to..."
"The candidate showed an ability to..."
"The candidate consistently demonstrated..."
"The candidate demonstrated a proactive approach..."

unless the statement is immediately supported by
specific evidence from the candidate.

For example, if the evidence states that the candidate
created a paid media plan after analysing the client's
requirements and executed it over three months, with the
first month used for testing, the rationale should refer
to those specific actions and timeline.

The rationale should answer:

"Why does this exact evidence justify this rating?"

Do not describe what the competency generally means.
Describe what THIS candidate actually did and why it
supports the rating.

Return ONLY valid JSON.

Return exactly:

{{
  "rating": 1,
  "rationale": "specific explanation grounded in the exact evidence",
  "confidence": 0.0
}}
"""

    def assess(
        self,
        competency_id: str,
        state: CompetencyState,
    ) -> EvidenceAssessment:

        if not state.evidence:

            return EvidenceAssessment(
                rating=EvidenceRating.INSUFFICIENT,
                rationale=(
                    "No behavioral evidence is "
                    "currently available."
                ),
                evidence_count=0,
                confidence=0.0,
            )

        prompt = self._build_prompt(
            competency_id,
            state,
        )

        raw_output = llm_client.generate(
            prompt
        )

        data = LLMParser.parse_json(
            raw_output
        )

        rating = EvidenceRating(
            int(data["rating"])
        )

        confidence = max(
            0.0,
            min(
                1.0,
                float(data["confidence"]),
            ),
        )

        assessment = EvidenceAssessment(
            rating=rating,
            rationale=str(
                data["rationale"]
            ),
            evidence_count=len(
                state.evidence
            ),
            confidence=confidence,
        )

        state.rating = int(rating)
        state.confidence = confidence
        state.assessment = assessment

        return assessment


assessment_engine = AssessmentEngine()