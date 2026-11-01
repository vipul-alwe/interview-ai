from fastapi import APIRouter

from app.core.interview_manager import manager


router = APIRouter()


@router.post("/start")
def start_interview():

    session = manager.create()

    return {
        "interview_id": session.interview_id,
        "competency_id": (
            session.current_question.competency_id
            if session.current_question
            else None
        ),
        "question": (
            session.current_question.question
            if session.current_question
            else None
        ),
    }