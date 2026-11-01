from app.core.interview_manager import manager
from app.engine.adaptive_question_engine import (
    adaptive_question_engine,
)


def main():

    session = manager.create()

    assert len(session.competencies) == 25

    competency_id, question = (
        adaptive_question_engine.select(
            session
        )
    )

    print(
        f"Selected competency: "
        f"{competency_id}"
    )

    print(
        f"Selected question: "
        f"{question}"
    )

    assert competency_id in (
        session.competencies
    )

    assert question

    assert (
        question
        in session.asked_questions
    )

    assert (
        session.current_question
        == question
    )

    first_question = question

    competency_id_2, question_2 = (
        adaptive_question_engine.select(
            session
        )
    )

    print(
        f"\nSecond competency: "
        f"{competency_id_2}"
    )

    print(
        f"Second question: "
        f"{question_2}"
    )

    assert question_2

    assert question_2 != first_question

    assert (
        len(session.asked_questions)
        == 2
    )

    print(
        "\nAdaptive question engine test passed."
    )


if __name__ == "__main__":
    main()