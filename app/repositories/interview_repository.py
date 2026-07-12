from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Interview


def get_user_interview(db: Session, interview_id: int, user_id: int) -> Interview | None:
    statement = (
        select(Interview)
        .where(Interview.id == interview_id, Interview.user_id == user_id)
        .options(selectinload(Interview.questions), selectinload(Interview.report))
    )
    return db.scalar(statement)


def list_user_interviews(db: Session, user_id: int) -> list[Interview]:
    statement = select(Interview).where(Interview.user_id == user_id).order_by(Interview.started_at.desc())
    return list(db.scalars(statement))

