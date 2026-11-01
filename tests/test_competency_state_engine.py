from app.domain.evidence import (
    Evidence,
    EvidencePolarity,
)
from app.engine.competency_state_engine import (
    competency_state_engine,
)
from app.engine.interview_competency_engine import (
    interview_competency_engine,
)


def main():

    states = (
        interview_competency_engine.initialize()
    )

    assert len(states) == 25

    evidence = [
        Evidence(
            competency_id="self_management",
            quote=(
                "I took ownership of the project."
            ),
            reasoning=(
                "The candidate demonstrated "
                "self-management."
            ),
            polarity=EvidencePolarity.POSITIVE,
            confidence=0.8,
            question_id="q1",
        ),
        Evidence(
            competency_id="planning_and_organizing",
            quote=(
                "I created a Gantt chart."
            ),
            reasoning=(
                "The candidate demonstrated "
                "planning."
            ),
            polarity=EvidencePolarity.POSITIVE,
            confidence=0.9,
            question_id="q1",
        ),
    ]

    states = competency_state_engine.apply(
        states,
        evidence,
    )

    self_management = states[
        "self_management"
    ]

    planning = states[
        "planning_and_organizing"
    ]

    assert len(
        self_management.evidence
    ) == 1

    assert len(
        planning.evidence
    ) == 1

    assert (
        self_management.confidence
        == 0.8
    )

    assert (
        planning.confidence
        == 0.9
    )

    assert (
        self_management.score
        == 1.0
    )

    assert (
        planning.score
        == 1.0
    )

    assert (
        self_management.coverage
        > 0.0
    )

    assert (
        planning.coverage
        > 0.0
    )

    assert (
        len(states) == 25
    )

    print(
        "25 competency states updated successfully."
    )

    print(
        f"Self-Management confidence: "
        f"{self_management.confidence:.2f}"
    )

    print(
        f"Planning confidence: "
        f"{planning.confidence:.2f}"
    )


if __name__ == "__main__":
    main()