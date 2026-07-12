from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    interview_id: Mapped[int] = mapped_column(ForeignKey("interviews.id"), index=True)
    local_question_id: Mapped[str] = mapped_column(String(120), index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    question_text: Mapped[str] = mapped_column(Text)
    expected_points: Mapped[list[str]] = mapped_column(JSON, default=list)
    keywords: Mapped[list[str]] = mapped_column(JSON, default=list)
    order_number: Mapped[int] = mapped_column(Integer, default=0)
    is_follow_up: Mapped[bool] = mapped_column(Boolean, default=False)
    parent_question_id: Mapped[int | None] = mapped_column(ForeignKey("interview_questions.id"), nullable=True)
    shown_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    interview = relationship("Interview", back_populates="questions")
    answer = relationship("Answer", back_populates="interview_question", uselist=False, cascade="all, delete-orphan")

