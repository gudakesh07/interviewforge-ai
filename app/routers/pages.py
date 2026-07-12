from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.repositories.interview_repository import list_user_interviews
from app.services.question_service import INTERVIEW_TYPES, LANGUAGES, LEVELS, PROFESSIONS
from app.services.statistics_service import get_statistics

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def index(request: Request, user: User | None = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user, "professions": PROFESSIONS})


@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db), user: User | None = Depends(get_current_user)):
    if user is None:
        return RedirectResponse("/login", status_code=303)
    interviews = list_user_interviews(db, user.id)
    stats = get_statistics(db, user.id)
    return templates.TemplateResponse(
        "dashboard/index.html",
        {"request": request, "user": user, "interviews": interviews[:8], "stats": stats},
    )


@router.get("/interviews/new")
def new_interview(request: Request, user: User | None = Depends(get_current_user)):
    if user is None:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(
        "interview/new.html",
        {
            "request": request,
            "user": user,
            "professions": PROFESSIONS,
            "levels": LEVELS,
            "languages": LANGUAGES,
            "interview_types": INTERVIEW_TYPES,
        },
    )
