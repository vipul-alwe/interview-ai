from pydantic import BaseModel, Field


class BehavioralEvent(BaseModel):
    id: str

    source_turns: list[int] = Field(
        default_factory=list
    )

    situation: str = ""

    action: str = ""

    result: str = ""

    quote: str = ""

    reasoning: str = ""