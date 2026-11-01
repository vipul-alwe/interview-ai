from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class EvidencePolarity(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class Evidence(BaseModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    competency_id: str

    quote: str

    reasoning: str

    polarity: EvidencePolarity

    confidence: float

    question_id: str

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )