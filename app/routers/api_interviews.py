from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_user
from app.models import User
from app.repositories.interview_repository import get_user_interview, list_user_interviews
from app.schemas.answer import AnswerCreate, AnswerOut
from app.schemas.auth import UserOut
from app.schemas.interview import InterviewCreate, InterviewOut
from app.services.interview_service import create_interview, current_question, finish_interview, save_answer
from app.services.report_service import create_report
from app.services.statistics_service import get_statistics

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(require_user)):
    return user


@router.get("/interviews", response_model=list[InterviewOut])
def api_interviews(db: Session = Depends(get_db), user: User = Depends(require_user)):
    return list_user_interviews(db, user.id)


@router.post("/interviews", response_model=InterviewOut, status_code=201)
def api_create_interview(payload: InterviewCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    return create_interview(
        db,
        user,
        payload.profession,
        payload.level,
        payload.interview_type,
        payload.language,
        payload.selected_technologies,
        payload.requested_question_count,
    )


@router.get("/interviews/{interview_id}", response_model=InterviewOut)
def api_get_interview(interview_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    interview = get_user_interview(db, interview_id, user.id)
    if interview is None:
        raise HTTPException(status_code=404)
    return interview


@router.post("/interviews/{interview_id}/answers", response_model=AnswerOut)
async def api_answer(interview_id: int, payload: AnswerCreate, db: Session = Depends(get_db), user: User = Depends(require_user)):
    interview = get_user_interview(db, interview_id, user.id)
    if interview is None:
        raise HTTPException(status_code=404)
    question = next((item for item in interview.questions if item.id == payload.question_id), current_question(interview))
    if question is None:
        raise HTTPException(status_code=400, detail="No active question")
    return await save_answer(db, interview, question, payload.answer_text)


@router.post("/interviews/{interview_id}/finish", response_model=InterviewOut)
def api_finish(interview_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    interview = get_user_interview(db, interview_id, user.id)
    if interview is None:
        raise HTTPException(status_code=404)
    return finish_interview(db, interview)


@router.get("/interviews/{interview_id}/report")
def api_report(interview_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    interview = get_user_interview(db, interview_id, user.id)
    if interview is None:
        raise HTTPException(status_code=404)
    return create_report(db, interview)


@router.get("/statistics")
def api_statistics(db: Session = Depends(get_db), user: User = Depends(require_user)):
    return get_statistics(db, user.id)

