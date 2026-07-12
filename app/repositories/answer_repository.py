from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Answer


def list_answers_for_interview(db: Session, interview_id: int) -> list[Answer]:
    statement = (
        select(Answer)
        .join(Answer.interview_question)
        .where(Answer.interview_question.has(interview_id=interview_id))
        .order_by(Answer.created_at)
    )
    return list(db.scalars(statement))

