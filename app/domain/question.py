from uuid import uuid4

from pydantic import BaseModel, Field


class Question(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    competency: str

    question: str

    follow_ups: list[str] = Field(default_factory=list)

    expected_indicators: list[str] = Field(default_factory=list)

    minimum_evidence: int = 3

    weight: float = 1.0