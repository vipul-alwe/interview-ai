from app.engine.interview_competency_engine import (
    interview_competency_engine,
)


def main():

    states = (
        interview_competency_engine.initialize()
    )

    print(
        f"Initialized states: {len(states)}"
    )

    assert len(states) == 25

    for competency_id, state in states.items():

        assert (
            competency_id
            == state.competency_id
        )

        assert state.coverage == 0.0
        assert state.score == 0.0
        assert state.rating is None
        assert state.evidence == []

    print(
        "\nAll 25 competency states initialized."
    )


if __name__ == "__main__":
    main()