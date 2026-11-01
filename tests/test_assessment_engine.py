from app.domain.evidence import (
    Evidence,
    EvidencePolarity,
)
from app.domain.competency_state import (
    CompetencyState,
)
from app.engine.assessment_engine import (
    assessment_engine,
)


def main():

    state = CompetencyState(
        competency_id="self_management",
        evidence=[
            Evidence(
                competency_id="self_management",
                quote=(
                    "My manager was unavailable, so I "
                    "created a Gantt chart with clear "
                    "timelines, prioritized the work, "
                    "coordinated with another HOD, and "
                    "we delivered the project three days early."
                ),
                reasoning=(
                    "The candidate independently organized "
                    "and prioritized work, maintained momentum "
                    "without direct supervision, and delivered "
                    "the desired outcome ahead of schedule."
                ),
                polarity=EvidencePolarity.POSITIVE,
                confidence=0.95,
                question_id="q1",
            ),
        ],
    )

    assessment = assessment_engine.assess(
        competency_id="self_management",
        state=state,
    )

    print(
        f"Rating: {assessment.rating.name}"
    )

    print(
        f"Score: {assessment.rating.value}/5"
    )

    print(
        f"Confidence: "
        f"{assessment.confidence:.2f}"
    )

    print(
        f"Evidence count: "
        f"{assessment.evidence_count}"
    )

    print(
        f"Rationale: "
        f"{assessment.rationale}"
    )

    assert assessment.rating is not None

    assert 1 <= assessment.rating.value <= 5

    assert assessment.evidence_count == 1

    assert 0.0 <= assessment.confidence <= 1.0

    assert state.rating == assessment.rating.value

    assert state.assessment is assessment

    print(
        "\nAssessment engine test passed."
    )


if __name__ == "__main__":
    main()