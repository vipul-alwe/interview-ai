from pydantic import BaseModel, Field


class TranscriptTurn(BaseModel):
    index: int
    text: str


class InterviewTranscript(BaseModel):
    turns: list[TranscriptTurn] = Field(
        default_factory=list
    )

    full_text: str = ""