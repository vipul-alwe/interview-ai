from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.competency_state import CompetencyState
from app.domain.generated_question import GeneratedQuestion
from app.domain.interview_context import InterviewContext


@dataclass
class InterviewSession:

    interview_id: str

    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    transcript: list[str] = field(
        default_factory=list
    )

    behaviours: dict = field(
        default_factory=dict
    )

    evidence: list = field(
        default_factory=list
    )

    metrics: dict = field(
        default_factory=dict
    )

    competencies: dict[
        str,
        CompetencyState,
    ] = field(
        default_factory=dict
    )

    context: InterviewContext = field(
        default_factory=InterviewContext
    )

    current_question: GeneratedQuestion | None = None