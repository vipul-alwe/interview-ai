from enum import IntEnum

from pydantic import BaseModel


class EvidenceRating(IntEnum):

    CONTRARY = 1
    INSUFFICIENT = 2
    SUFFICIENT = 3
    NUMEROUS = 4
    ROLE_MODEL = 5


class EvidenceAssessment(BaseModel):

    rating: EvidenceRating | None = None

    rationale: str = ""

    evidence_count: int = 0

    confidence: float = 0.0