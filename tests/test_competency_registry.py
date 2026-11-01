from app.registry.competency_registry import (
    competency_registry,
)


def main():

    print(
        f"Registry count: "
        f"{competency_registry.count()}"
    )

    assert (
        competency_registry.count()
        == 25
    )

    print("\nRegistered competencies:")

    for competency in (
        competency_registry.all()
    ):

        print(
            f"- {competency.id}: "
            f"{competency.name}"
        )

    assert (
        competency_registry.get(
            "results_orientation"
        )
        is not None
    )

    assert (
        competency_registry.get(
            "creativity"
        )
        is not None
    )

    assert (
        competency_registry.get(
            "does_not_exist"
        )
        is None
    )

    print(
        "\nAll competency registry tests passed."
    )


if __name__ == "__main__":
    main()