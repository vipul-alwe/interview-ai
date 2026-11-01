from uuid import uuid4

from app.domain.generated_question import GeneratedQuestion
from app.engine.interview_competency_engine import (
    interview_competency_engine,
)

from .session import InterviewSession


class InterviewManager:

    def __init__(self):
        self.sessions = {}

    def create(self):

        interview_id = str(uuid4())

        competencies = (
            interview_competency_engine.initialize()
        )

        session = InterviewSession(
            interview_id=interview_id,
            competencies=competencies,
        )

        session.current_question = GeneratedQuestion(
            competency_id="",
            target_indicators=[],
            question=(
                "Tell me about a project or piece of "
                "work you're particularly proud of."
            ),
            intent=(
                "Open the interview and identify "
                "a useful behavioral story."
            ),
            context="Initial interview question.",
            follow_up_to=None,
        )

        session.context.current_topic = (
            "candidate background and experience"
        )

        self.sessions[interview_id] = session

        print(
            "[INTERVIEW] Initial question: "
            f"{session.current_question.question}"
        )

        return session

    def get(
        self,
        interview_id: str,
    ):
        return self.sessions.get(interview_id)


manager = InterviewManager()