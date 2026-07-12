from app.services.ai.base import AIContext, BaseAIProvider
from app.services.evaluation.local_evaluator import EvaluationResult, evaluate_locally


class MockAIProvider(BaseAIProvider):
    name = "mock"

    async def evaluate_answer(self, context: AIContext) -> EvaluationResult:
        result = evaluate_locally(context.answer, context.keywords, context.expected_points)
        result.source = "mock-ai"
        return result

    async def generate_follow_up(self, context: AIContext, missed_points: list[str]) -> str:
        if missed_points:
            return f"Could you expand on this point: {missed_points[0]}?"
        return "Could you add a practical example from real work?"

    async def generate_final_report(self, summary: str, language: str) -> str:
        return summary

