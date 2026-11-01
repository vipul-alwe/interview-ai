from app.core.session import InterviewSession
from app.domain.competency_state import CompetencyState
from app.registry.competency_registry import competency_registry


class AdaptiveQuestionEngine:

    def select(
        self,
        session: InterviewSession,
    ) -> tuple[str, str] | None:

        candidates = []

        for competency_id, state in (
            session.competencies.items()
        ):

            if not state.evidence:
                priority = 1.0

            else:
                priority = (
                    (1.0 - state.coverage)
                    * (1.0 - state.confidence)
                )

            candidates.append(
                (
                    priority,
                    competency_id,
                )
            )

        if not candidates:
            return None

        _, competency_id = max(
            candidates,
            key=lambda item: item[0],
        )

        competency = competency_registry.get(
            competency_id
        )

        if competency is None:
            return None

        for question in competency.questions:

            if question not in session.asked_questions:

                session.current_question = question

                session.asked_questions.append(
                    question
                )

                return (
                    competency_id,
                    question,
                )

        return None


adaptive_question_engine = (
    AdaptiveQuestionEngine()
)