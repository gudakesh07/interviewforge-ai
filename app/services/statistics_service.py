from sqlalchemy.orm import Session

from app.repositories.interview_repository import list_user_interviews


def get_statistics(db: Session, user_id: int) -> dict:
    interviews = list_user_interviews(db, user_id)
    completed = [interview for interview in interviews if interview.status == "completed"]
    scores = [interview.total_score for interview in completed]
    return {
        "interview_count": len(interviews),
        "completed_count": len(completed),
        "average_score": round(sum(scores) / len(scores), 2) if scores else 0,
        "best_score": max(scores) if scores else 0,
        "completion_rate": round(len(completed) / len(interviews) * 100, 2) if interviews else 0,
        "progress": [{"date": item.started_at.date().isoformat(), "score": item.total_score} for item in completed],
    }

