from datetime import datetime

from sqlalchemy.orm import Session

from app.config import settings
from app.models import Answer, Interview, InterviewQuestion, User
from app.services.ai.base import AIContext
from app.services.ai.factory import get_ai_provider
from app.services.evaluation.local_evaluator import evaluate_locally
from app.services.question_service import select_questions
from app.utils.dates import seconds_between
from app.utils.validators import clean_text


def create_interview(
    db: Session,
    user: User,
    profession: str,
    level: str,
    interview_type: str,
    language: str,
    technologies: list[str],
    question_count: int,
) -> Interview:
    count = min(question_count, settings.max_interview_questions)
    if interview_type == "quick":
        count = min(count, 5)
    questions = select_questions(profession, level, technologies, count, interview_type)
    interview = Interview(
        user_id=user.id,
        profession=profession,
        level=level,
        interview_type=interview_type,
        language=language,
        selected_technologies=technologies,
        requested_question_count=count,
        status="in_progress",
    )
    db.add(interview)
    db.flush()
    for index, question in enumerate(questions, start=1):
        db.add(
            InterviewQuestion(
                interview_id=interview.id,
                local_question_id=question.id,
                category=question.category,
                question_text=question.question.get(language) or question.question["en"],
                expected_points=question.expected_points,
                keywords=question.keywords,
                order_number=index,
            )
        )
    db.commit()
    db.refresh(interview)
    return interview


def current_question(interview: Interview) -> InterviewQuestion | None:
    questions = sorted(interview.questions, key=lambda item: item.order_number)
    for question in questions:
        if question.answer is None:
            return question
    return None


async def save_answer(db: Session, interview: Interview, question: InterviewQuestion, answer_text: str) -> Answer:
    cleaned = clean_text(answer_text, settings.max_answer_length)
    provider = get_ai_provider()
    context = AIContext(
        question=question.question_text,
        expected_points=question.expected_points,
        keywords=question.keywords,
        answer=cleaned,
        level=interview.level,
        profession=interview.profession,
        language=interview.language,
    )
    try:
        result = await provider.evaluate_answer(context)
    except Exception:
        result = evaluate_locally(cleaned, question.keywords, question.expected_points)

    answer = Answer(
        interview_question_id=question.id,
        answer_text=cleaned,
        score=result.score,
        feedback=result.feedback,
        strengths=result.strengths,
        weaknesses=result.weaknesses,
        missed_points=result.missed_points,
        evaluation_source=result.source,
        response_time_seconds=seconds_between(question.shown_at),
    )
    db.add(answer)
    db.flush()

    if result.score < 70 and not question.is_follow_up:
        follow_up_text = await provider.generate_follow_up(context, result.missed_points)
        db.add(
            InterviewQuestion(
                interview_id=interview.id,
                local_question_id=f"{question.local_question_id}_follow_up",
                category=question.category,
                question_text=follow_up_text,
                expected_points=result.missed_points or question.expected_points[:1],
                keywords=question.keywords,
                order_number=question.order_number + 1000,
                is_follow_up=True,
                parent_question_id=question.id,
            )
        )
    interview.current_question_index += 1
    db.commit()
    db.refresh(answer)
    return answer


def finish_interview(db: Session, interview: Interview) -> Interview:
    answers = [question.answer for question in interview.questions if question.answer is not None]
    interview.status = "completed"
    interview.completed_at = datetime.utcnow()
    interview.duration_seconds = seconds_between(interview.started_at, interview.completed_at)
    interview.total_score = round(sum(answer.score for answer in answers) / len(answers), 2) if answers else 0
    db.commit()
    db.refresh(interview)
    return interview

