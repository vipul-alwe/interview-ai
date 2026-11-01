from pydantic import BaseModel

from app.schemas.evidence_candidate import (
    EvidenceCandidate,
)


class LLMEvidenceResponse(BaseModel):

    evidence: list[EvidenceCandidate]