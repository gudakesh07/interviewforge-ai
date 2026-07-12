import httpx

from app.config import settings
from app.services.ai.base import AIContext, BaseAIProvider, build_evaluation_prompt, parse_ai_evaluation


class OllamaProvider(BaseAIProvider):
    name = "ollama"

    async def evaluate_answer(self, context: AIContext):
        async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
            response = await client.post(
                f"{settings.ollama_base_url.rstrip('/')}/api/generate",
                json={"model": settings.ollama_model, "prompt": build_evaluation_prompt(context), "stream": False},
            )
            response.raise_for_status()
            text = response.json().get("response", "")
            result = parse_ai_evaluation(text)
            result.source = self.name
            return result

    async def generate_follow_up(self, context: AIContext, missed_points: list[str]) -> str:
        point = missed_points[0] if missed_points else "a real project example"
        return f"What would change if you applied {point} in production?"

    async def generate_final_report(self, summary: str, language: str) -> str:
        return summary
