from uuid import uuid4

from pydantic import BaseModel, Field


class GeneratedQuestion(BaseModel):

    question_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    competency_id: str

    target_indicators: list[str] = Field(
        default_factory=list
    )

    question: str

    intent: str = ""

    context: str = ""

    follow_up_to: str | None = None