from app.domain.competency_state import CompetencyState
from app.registry.competency_registry import (
    competency_registry,
)


class InterviewCompetencyEngine:

    def initialize(self) -> dict[
        str,
        CompetencyState,
    ]:

        states = {}

        for competency in competency_registry.all():

            states[competency.id] = (
                CompetencyState(
                    competency_id=competency.id,
                )
            )

        return states


interview_competency_engine = (
    InterviewCompetencyEngine()
)