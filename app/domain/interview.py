from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field

from app.domain.competency_state import CompetencyState
from app.domain.evidence import Evidence
from app.domain.response import Response


class Interview(BaseModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    candidate_name: str | None = None

    interviewer_name: str | None = None

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    ended_at: datetime | None = None

    current_question: str | None = None

    transcript: list[str] = Field(
        default_factory=list
    )

    responses: list[Response] = Field(
        default_factory=list
    )

    evidence: list[Evidence] = Field(
        default_factory=list
    )

    competencies: dict[
        str,
        CompetencyState,
    ] = Field(
        default_factory=dict
    )