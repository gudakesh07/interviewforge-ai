from collections import defaultdict

from sqlalchemy.orm import Session

from app.models import FinalReport, Interview
from app.services.interview_service import finish_interview


def _category_scores(interview: Interview) -> dict[str, list[float]]:
    scores: dict[str, list[float]] = defaultdict(list)
    for question in interview.questions:
        if question.answer:
            scores[question.category].append(question.answer.score)
    return scores


def build_study_plan(weak_categories: list[str]) -> list[dict]:
    categories = weak_categories or ["core concepts", "practical explanations", "communication"]
    return [
        {
            "day": day,
            "topic": categories[(day - 1) % len(categories)],
            "tasks": [
                "Review theory and write a short summary.",
                "Practice 5 focused interview questions.",
                "Explain one real-world example aloud.",
            ],
        }
        for day in range(1, 8)
    ]


def create_report(db: Session, interview: Interview) -> FinalReport:
    if interview.status != "completed":
        finish_interview(db, interview)
    if interview.report:
        return interview.report

    grouped = _category_scores(interview)
    averages = {category: sum(scores) / len(scores) for category, scores in grouped.items() if scores}
    strong = [category for category, score in averages.items() if score >= 75]
    weak = [category for category, score in averages.items() if score < 70]
    recommendations = [
        f"Повторить тему {category}: ключевые определения, примеры и типовые ошибки."
        for category in (weak or list(averages)[:3])
    ]
    if not recommendations:
        recommendations = ["Сделать ещё одно интервью на более высоком уровне сложности."]

    report = FinalReport(
        interview_id=interview.id,
        overall_score=interview.total_score,
        technical_score=interview.total_score,
        communication_score=round(min(100, interview.total_score + 5), 2),
        strong_categories=strong,
        weak_categories=weak,
        recommendations=recommendations,
        study_plan=build_study_plan(weak),
        summary=f"Итоговый результат: {interview.total_score}/100. Сильные темы: {', '.join(strong) or 'пока не выявлены'}.",
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

