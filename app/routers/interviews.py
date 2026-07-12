from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.repositories.interview_repository import get_user_interview
from app.services.interview_service import create_interview, current_question, finish_interview, save_answer
from app.services.report_service import create_report

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/interviews")
def create_interview_route(
    profession: str = Form(...),
    level: str = Form(...),
    interview_type: str = Form("technical"),
    language: str = Form("ru"),
    technologies: list[str] = Form(default=[]),
    requested_question_count: int = Form(5),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user),
):
    if user is None:
        return RedirectResponse("/login", status_code=303)
    interview = create_interview(db, user, profession, level, interview_type, language, technologies, requested_question_count)
    return RedirectResponse(f"/interviews/{interview.id}", status_code=303)


@router.get("/interviews/{interview_id}")
def show_interview(interview_id: int, request: Request, db: Session = Depends(get_db), user: User | None = Depends(get_current_user)):
    if user is None:
        return RedirectResponse("/login", status_code=303)
    interview = get_user_interview(db, interview_id, user.id)
    if interview is None:
        raise HTTPException(status_code=404)
    question = current_question(interview)
    if question is None:
        return RedirectResponse(f"/interviews/{interview.id}/finish", status_code=303)
    return templates.TemplateResponse("interview/show.html", {"request": request, "user": user, "interview": interview, "question": question})


@router.post("/interviews/{interview_id}/answers")
async def submit_answer(
    interview_id: int,
    question_id: int = Form(...),
    answer_text: str = Form(...),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user),
):
    if user is None:
        return RedirectResponse("/login", status_code=303)
    interview = get_user_interview(db, interview_id, user.id)
    if interview is None:
        raise HTTPException(status_code=404)
    question = next((item for item in interview.questions if item.id == question_id), None)
    if question is None or question.answer is not None:
        raise HTTPException(status_code=400, detail="Question is not available")
    await save_answer(db, interview, question, answer_text)
    return RedirectResponse(f"/interviews/{interview.id}", status_code=303)


@router.get("/interviews/{interview_id}/finish")
def finish_page(interview_id: int, db: Session = Depends(get_db), user: User | None = Depends(get_current_user)):
    if user is None:
        return RedirectResponse("/login", status_code=303)
    interview = get_user_interview(db, interview_id, user.id)
    if interview is None:
        raise HTTPException(status_code=404)
    finish_interview(db, interview)
    create_report(db, interview)
    return RedirectResponse(f"/reports/{interview.id}", status_code=303)

