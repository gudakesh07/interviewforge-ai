from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    profession: Mapped[str] = mapped_column(String(60), index=True)
    level: Mapped[str] = mapped_column(String(30), index=True)
    interview_type: Mapped[str] = mapped_column(String(40), default="technical")
    language: Mapped[str] = mapped_column(String(8), default="ru")
    selected_technologies: Mapped[list[str]] = mapped_column(JSON, default=list)
    requested_question_count: Mapped[int] = mapped_column(Integer, default=5)
    current_question_index: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="created", index=True)
    total_score: Mapped[float] = mapped_column(Float, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0)

    user = relationship("User", back_populates="interviews")
    questions = relationship("InterviewQuestion", back_populates="interview", cascade="all, delete-orphan")
    report = relationship("FinalReport", back_populates="interview", uselist=False, cascade="all, delete-orphan")

