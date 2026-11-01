from pydantic import BaseModel, Field

from app.domain.evidence import Evidence
from app.domain.evidence_assessment import EvidenceAssessment


class CompetencyState(BaseModel):

    competency_id: str

    score: float = 0.0

    rating: int | None = None

    confidence: float = 0.0

    coverage: float = 0.0

    evidence: list[Evidence] = Field(
        default_factory=list
    )

    follow_up_questions: list[str] = Field(
        default_factory=list
    )

    assessment: EvidenceAssessment | None = None