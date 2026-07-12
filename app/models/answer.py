from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    interview_question_id: Mapped[int] = mapped_column(ForeignKey("interview_questions.id"), index=True)
    answer_text: Mapped[str] = mapped_column(Text)
    score: Mapped[float] = mapped_column(Float, default=0)
    feedback: Mapped[str] = mapped_column(Text)
    strengths: Mapped[list[str]] = mapped_column(JSON, default=list)
    weaknesses: Mapped[list[str]] = mapped_column(JSON, default=list)
    missed_points: Mapped[list[str]] = mapped_column(JSON, default=list)
    evaluation_source: Mapped[str] = mapped_column(String(40), default="local")
    response_time_seconds: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    interview_question = relationship("InterviewQuestion", back_populates="answer")

