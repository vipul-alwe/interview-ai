from app.core.interview_manager import (
    InterviewManager,
)


def main():

    manager = InterviewManager()

    session = manager.create()

    print(
        f"Interview ID: "
        f"{session.interview_id}"
    )

    print(
        f"Competency states: "
        f"{len(session.competencies)}"
    )

    assert len(
        session.competencies
    ) == 25

    assert (
        session.competencies[
            "results_orientation"
        ].competency_id
        == "results_orientation"
    )

    assert (
        session.competencies[
            "creativity"
        ].competency_id
        == "creativity"
    )

    retrieved = manager.get(
        session.interview_id
    )

    assert retrieved is session

    print(
        "\nInterview session correctly "
        "contains all 25 competency states."
    )


if __name__ == "__main__":
    main()