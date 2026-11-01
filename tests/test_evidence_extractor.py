from datetime import datetime, timezone
import asyncio

from app.domain.response import Response
from app.engine.evidence_extractor import evidence_extractor
from app.registry.competency_registry import competency_registry


def main():

    print("Loading competency registry...")

    competencies = competency_registry.all()

    print(
        f"Competencies available: "
        f"{len(competencies)}"
    )

    assert len(competencies) == 25

    response = Response(
        question_id="test_question_001",
        transcript=(
            "My manager was unavailable, so I took ownership "
            "of the project. I created a Gantt chart with clear "
            "timelines, coordinated with another HOD, and we "
            "delivered the project three days early. One risk "
            "was that the project depended on another department, "
            "so I contacted them early to make sure we stayed "
            "on schedule."
        ),
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        duration=20.0,
    )

    evidence = asyncio.run(
        evidence_extractor.extract(
            response=response,
        )
    )

    print(
        f"\nEvidence extracted: {len(evidence)}"
    )

    for item in evidence:

        print(
            f"\nCompetency: "
            f"{item.competency_id}"
        )

        print(
            f"Polarity: "
            f"{item.polarity.value}"
        )

        print(
            f"Confidence: "
            f"{item.confidence:.2f}"
        )

        print(
            f"Quote: "
            f"{item.quote}"
        )

        print(
            f"Reasoning: "
            f"{item.reasoning}"
        )

    valid_competency_ids = {
        competency.id
        for competency in competencies
    }

    for item in evidence:

        assert (
            item.competency_id
            in valid_competency_ids
        )

        assert item.quote
        assert item.reasoning

        assert (
            0.0
            <= item.confidence
            <= 1.0
        )

        assert item.question_id == (
            response.question_id
        )

    print(
        "\nEvidence extraction test passed."
    )


if __name__ == "__main__":
    main()