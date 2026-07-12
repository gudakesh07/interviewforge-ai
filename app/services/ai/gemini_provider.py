import httpx

from app.config import settings
from app.services.ai.base import AIContext, BaseAIProvider, build_evaluation_prompt, parse_ai_evaluation


class GeminiProvider(BaseAIProvider):
    name = "gemini"

    async def evaluate_answer(self, context: AIContext):
        model = settings.gemini_model or "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
            response = await client.post(
                url,
                params={"key": settings.gemini_api_key},
                json={"contents": [{"parts": [{"text": build_evaluation_prompt(context)}]}]},
            )
            response.raise_for_status()
            text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            result = parse_ai_evaluation(text)
            result.source = self.name
            return result

    async def generate_follow_up(self, context: AIContext, missed_points: list[str]) -> str:
        point = missed_points[0] if missed_points else "one concrete example"
        return f"Please add more detail about {point}."

    async def generate_final_report(self, summary: str, language: str) -> str:
        return summary
