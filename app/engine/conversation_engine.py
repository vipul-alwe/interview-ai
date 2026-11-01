import json

from app.core.session import InterviewSession
from app.domain.generated_question import GeneratedQuestion
from app.llm.client import llm_client
from app.llm.parser import LLMParser
from app.registry.competency_registry import competency_registry


class ConversationEngine:

    def _build_prompt(
        self,
        session: InterviewSession,
    ) -> str:

        competency_text = []

        for competency_id, state in (
            session.competencies.items()
        ):

            competency = competency_registry.get(
                competency_id
            )

            if competency is None:
                continue

            evidence = [
                {
                    "quote": item.quote,
                    "reasoning": item.reasoning,
                    "confidence": item.confidence,
                    "polarity": item.polarity.value,
                }
                for item in state.evidence
            ]

            competency_text.append(
                {
                    "id": competency.id,
                    "name": competency.name,
                    "description": competency.description,
                    "confidence": state.confidence,
                    "coverage": state.coverage,
                    "rating": state.rating,
                    "evidence": evidence,
                }
            )

        return f"""
You are the conversational controller of a behavioral interview.

Generate the SINGLE most natural next interview question.

This is a real conversational interview, NOT a questionnaire.

Use:
- the candidate's previous answer
- the current conversation topic
- existing evidence
- competency coverage
- competency ratings
- evidence gaps

Prefer a natural follow-up to the candidate's current story
when that can reveal additional behavioral evidence.

Only move to another competency when the current thread has
little additional value or another competency is substantially
less explored.

Do not repeat something the candidate has already answered.

Do not invent candidate facts.

The question should be open-ended and behavioral.

INTERVIEW CONTEXT

Previous question:
{session.context.last_question}

Previous response:
{session.context.last_response}

Current topic:
{session.context.current_topic}

Conversation summary:
{session.context.conversation_summary}

Unanswered threads:
{json.dumps(session.context.unanswered_threads)}

Turn count:
{session.context.turn_count}

COMPETENCY STATES

{json.dumps(competency_text, indent=2)}

Return ONLY valid JSON:

{{
    "competency_id": "one valid competency ID",
    "target_indicators": [],
    "question": "natural conversational question",
    "intent": "what the question is trying to establish",
    "context": "why this question naturally follows",
    "follow_up_to": "specific part of the previous response"
}}

Rules:

- competency_id must be valid.
- target_indicators may be empty.
- question must sound conversational.
- Do not mention competency names to the candidate.
- Do not ask a generic unrelated question.
- Do not repeat the previous question.
- Do not fabricate candidate details.
"""

    def generate(
        self,
        session: InterviewSession,
    ) -> GeneratedQuestion:

        prompt = self._build_prompt(session)

        raw = llm_client.generate(prompt)

        data = LLMParser.parse_json(raw)

        question = GeneratedQuestion.model_validate(data)

        session.current_question = question

        return question


conversation_engine = ConversationEngine()