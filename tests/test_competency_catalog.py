from app.domain.competency_catalog import (
    get_all_competencies,
    get_competency,
)


def main():

    competencies = get_all_competencies()

    print(
        f"Total competencies: {len(competencies)}"
    )

    assert len(competencies) == 25

    print("\nCompetencies:")

    for index, competency in enumerate(
        competencies,
        start=1,
    ):

        print(
            f"{index:02d}. "
            f"{competency.id} | "
            f"{competency.name} | "
            f"{len(competency.questions)} questions"
        )

    print("\nTesting lookup:")

    result = get_competency(
        "results_orientation"
    )

    assert result is not None
    assert result.name == "Results Orientation"

    print(
        f"Lookup successful: "
        f"{result.name}"
    )

    print("\nTesting missing competency:")

    result = get_competency(
        "does_not_exist"
    )

    assert result is None

    print(
        "Missing competency correctly "
        "returns None."
    )

    print("\nAll competency catalog tests passed.")


if __name__ == "__main__":
    main()