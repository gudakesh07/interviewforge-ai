from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.repositories.interview_repository import get_user_interview
from app.services.pdf_service import build_report_pdf
from app.services.report_service import create_report

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/reports/{interview_id}")
def report_page(interview_id: int, request: Request, db: Session = Depends(get_db), user: User | None = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=401)
    interview = get_user_interview(db, interview_id, user.id)
    if interview is None:
        raise HTTPException(status_code=404)
    report = create_report(db, interview)
    return templates.TemplateResponse("reports/show.html", {"request": request, "user": user, "interview": interview, "report": report})


@router.get("/reports/{interview_id}/pdf")
def report_pdf(interview_id: int, db: Session = Depends(get_db), user: User | None = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=401)
    interview = get_user_interview(db, interview_id, user.id)
    if interview is None:
        raise HTTPException(status_code=404)
    report = create_report(db, interview)
    pdf = build_report_pdf(user, interview, report)
    return Response(pdf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=interviewforge-report.pdf"})

