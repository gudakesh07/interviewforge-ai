import random
from dataclasses import dataclass
from pathlib import Path

from app.config import settings
from app.utils.json_helpers import read_json

PROFESSIONS = {
    "python": ["Python Core", "OOP", "FastAPI", "Django", "SQL", "Testing", "Async Python", "Docker"],
    "java": ["Java Core", "OOP", "Spring", "SQL", "Concurrency", "Testing"],
    "javascript": ["JavaScript Core", "DOM", "Async JS", "REST API", "Testing"],
    "backend": ["REST API", "Databases", "Architecture", "Security", "Docker"],
    "frontend": ["HTML", "CSS", "Accessibility", "Browser APIs", "Performance"],
    "qa": ["Testing theory", "Test cases", "Automation", "API testing", "Bugs"],
    "devops": ["Linux", "Docker", "CI/CD", "Networking", "Monitoring"],
    "data_analyst": ["SQL", "Statistics", "Python", "Visualization", "Product metrics"],
    "hr": ["Motivation", "Teamwork", "Conflict", "Leadership", "Communication"],
    "general": ["Algorithms", "Git", "System Design", "Databases", "Communication"],
}
LEVELS = ["intern", "junior", "middle", "senior"]
LANGUAGES = {"ru": "Russian", "en": "English", "uk": "Ukrainian"}
INTERVIEW_TYPES = ["technical", "hr", "mixed", "quick", "full"]


@dataclass(slots=True)
class LocalQuestion:
    id: str
    profession: str
    level: str
    category: str
    question: dict[str, str]
    keywords: list[str]
    expected_points: list[str]
    difficulty: int
    max_score: int


def load_questions() -> list[LocalQuestion]:
    questions: list[LocalQuestion] = []
    for path in sorted(Path(settings.question_data_dir).glob("*.json")):
        for raw in read_json(path):
            questions.append(LocalQuestion(**raw))
    return questions


def select_questions(
    profession: str,
    level: str,
    technologies: list[str],
    count: int,
    interview_type: str,
) -> list[LocalQuestion]:
    pool = load_questions()
    normalized_profession = profession.lower()
    normalized_level = level.lower()
    tech_terms = {item.lower().replace(" ", "_") for item in technologies}
    selected = [
        question
        for question in pool
        if question.level.lower() in {normalized_level, "junior", "middle"}
        and (question.profession == normalized_profession or question.profession == "general")
    ]
    if interview_type == "hr":
        selected = [question for question in pool if question.profession == "hr"]
    elif interview_type == "mixed":
        selected += [question for question in pool if question.profession == "hr"]
    if tech_terms:
        selected.sort(key=lambda question: question.category.lower() not in tech_terms)
    if not selected:
        selected = pool
    random.shuffle(selected)
    return selected[:count]

