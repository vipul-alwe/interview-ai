from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from app.domain.evidence import Evidence
from app.domain.transcript_segment import TranscriptSegment


class Response(BaseModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    question_id: str

    transcript: str

    segments: list[TranscriptSegment] = Field(
        default_factory=list
    )

    started_at: datetime

    ended_at: datetime

    duration: float

    speech_features: dict[str, float] = Field(
        default_factory=dict
    )

    evidence: list[Evidence] = Field(
        default_factory=list
    )

    metadata: dict = Field(
        default_factory=dict
    )