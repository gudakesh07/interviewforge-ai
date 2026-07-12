from app.database import SessionLocal
from app.repositories.user_repository import create_user
from app.services.interview_service import create_interview, current_question, save_answer
from app.services.pdf_service import build_report_pdf
from app.services.report_service import create_report


async def test_pdf_report_generation():
    with SessionLocal() as db:
        user = create_user(db, "pdfuser", "pdf@example.com", "strong-password")
        interview = create_interview(db, user, "python", "junior", "quick", "en", [], 1)
        question = current_question(interview)
        await save_answer(db, interview, question, "A list is mutable and a tuple is immutable.")
        report = create_report(db, interview)
        pdf = build_report_pdf(user, interview, report)
    assert pdf.startswith(b"%PDF")

