from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class FinalReport(Base):
    __tablename__ = "final_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    interview_id: Mapped[int] = mapped_column(ForeignKey("interviews.id"), unique=True, index=True)
    overall_score: Mapped[float] = mapped_column(Float, default=0)
    technical_score: Mapped[float] = mapped_column(Float, default=0)
    communication_score: Mapped[float] = mapped_column(Float, default=0)
    strong_categories: Mapped[list[str]] = mapped_column(JSON, default=list)
    weak_categories: Mapped[list[str]] = mapped_column(JSON, default=list)
    recommendations: Mapped[list[str]] = mapped_column(JSON, default=list)
    study_plan: Mapped[list[dict]] = mapped_column(JSON, default=list)
    summary: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    interview = relationship("Interview", back_populates="report")

