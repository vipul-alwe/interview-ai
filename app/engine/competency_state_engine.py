from app.domain.competency_state import CompetencyState
from app.domain.evidence import Evidence


class CompetencyStateEngine:

    def apply(
        self,
        states: dict[str, CompetencyState],
        evidence: list[Evidence],
    ) -> dict[str, CompetencyState]:

        for item in evidence:

            state = states.get(
                item.competency_id
            )

            if state is None:
                continue

            state.evidence.append(item)

            state.confidence = self._confidence(
                state
            )

            state.coverage = self._coverage(
                state
            )

            state.score = self._score(
                state
            )

        return states

    @staticmethod
    def _confidence(
        state: CompetencyState,
    ) -> float:

        if not state.evidence:
            return 0.0

        return sum(
            item.confidence
            for item in state.evidence
        ) / len(state.evidence)

    @staticmethod
    def _coverage(
        state: CompetencyState,
    ) -> float:

        if not state.evidence:
            return 0.0

        return min(
            len(state.evidence) / 3.0,
            1.0,
        )

    @staticmethod
    def _score(
        state: CompetencyState,
    ) -> float:

        if not state.evidence:
            return 0.0

        positive = sum(
            item.confidence
            for item in state.evidence
            if item.polarity.value == "positive"
        )

        negative = sum(
            item.confidence
            for item in state.evidence
            if item.polarity.value == "negative"
        )

        total = positive + negative

        if total == 0:
            return 0.0

        return positive / total


competency_state_engine = CompetencyStateEngine()