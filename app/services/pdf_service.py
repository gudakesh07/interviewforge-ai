from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.models import FinalReport, Interview, User


def build_report_pdf(user: User, interview: Interview, report: FinalReport) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="InterviewForge AI Report")
    styles = getSampleStyleSheet()
    story = [
        Paragraph("InterviewForge AI Report", styles["Title"]),
        Paragraph(f"User: {user.username}", styles["Normal"]),
        Paragraph(f"Interview: {interview.profession} / {interview.level}", styles["Normal"]),
        Paragraph(f"Overall score: {report.overall_score}/100", styles["Heading2"]),
        Spacer(1, 12),
        Paragraph(report.summary, styles["BodyText"]),
        Spacer(1, 12),
    ]
    table_data = [["Question", "Category", "Score"]]
    for question in sorted(interview.questions, key=lambda item: item.order_number):
        score = question.answer.score if question.answer else 0
        table_data.append([question.question_text[:70], question.category, str(score)])
    table = Table(table_data, colWidths=[320, 100, 60])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#24324a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 12))
    story.append(Paragraph("Recommendations", styles["Heading2"]))
    for recommendation in report.recommendations:
        story.append(Paragraph(f"- {recommendation}", styles["BodyText"]))
    doc.build(story)
    return buffer.getvalue()

