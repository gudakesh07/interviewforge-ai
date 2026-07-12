import json
import re
from dataclasses import dataclass

from app.services.evaluation.local_evaluator import EvaluationResult


@dataclass(slots=True)
class AIContext:
    question: str
    expected_points: list[str]
    keywords: list[str]
    answer: str
    level: str
    profession: str
    language: str


class BaseAIProvider:
    name = "base"

    async def evaluate_answer(self, context: AIContext) -> EvaluationResult:
        raise NotImplementedError

    async def generate_follow_up(self, context: AIContext, missed_points: list[str]) -> str:
        raise NotImplementedError

    async def generate_final_report(self, summary: str, language: str) -> str:
        raise NotImplementedError


def build_evaluation_prompt(context: AIContext) -> str:
    return (
        "Evaluate an interview answer. Return compact JSON with keys: "
        "score, feedback, strengths, weaknesses, missed_points. "
        f"Profession: {context.profession}. Level: {context.level}. Language: {context.language}. "
        f"Question: {context.question}. Expected points: {context.expected_points}. "
        f"Keywords: {context.keywords}. Answer: {context.answer}"
    )


def parse_ai_evaluation(text: str) -> EvaluationResult:
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    data = json.loads(match.group(0) if match else text)
    return EvaluationResult(
        score=float(data.get("score", 0)),
        feedback=str(data.get("feedback", "AI evaluation completed.")),
        strengths=list(data.get("strengths", [])),
        weaknesses=list(data.get("weaknesses", [])),
        missed_points=list(data.get("missed_points", [])),
        source="ai",
    )
