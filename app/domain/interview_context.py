from pydantic import BaseModel, Field


class InterviewContext(BaseModel):

    conversation_summary: str = ""

    last_question: str | None = None

    last_response: str | None = None

    current_topic: str | None = None

    candidate_claims: list[str] = Field(
        default_factory=list
    )

    unanswered_threads: list[str] = Field(
        default_factory=list
    )

    topics_discussed: list[str] = Field(
        default_factory=list
    )

    turn_count: int = 0