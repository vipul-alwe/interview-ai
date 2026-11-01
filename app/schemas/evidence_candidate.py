from app.domain.evidence import EvidencePolarity
from pydantic import BaseModel


class EvidenceCandidate(BaseModel):

    competency_id: str

    quote: str

    reasoning: str

    polarity: EvidencePolarity

    confidence: float