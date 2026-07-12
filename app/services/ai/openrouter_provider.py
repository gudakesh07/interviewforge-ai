import httpx

from app.config import settings
from app.services.ai.base import AIContext, BaseAIProvider, build_evaluation_prompt, parse_ai_evaluation


class OpenRouterProvider(BaseAIProvider):
    name = "openrouter"

    async def evaluate_answer(self, context: AIContext):
        async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.openrouter_api_key}",
                    "HTTP-Referer": settings.app_url,
                    "X-Title": settings.app_name,
                },
                json={
                    "model": settings.openrouter_model or "openai/gpt-4o-mini",
                    "messages": [{"role": "user", "content": build_evaluation_prompt(context)}],
                    "temperature": 0.2,
                },
            )
            response.raise_for_status()
            text = response.json()["choices"][0]["message"]["content"]
            result = parse_ai_evaluation(text)
            result.source = self.name
            return result

    async def generate_follow_up(self, context: AIContext, missed_points: list[str]) -> str:
        point = missed_points[0] if missed_points else "a practical example"
        return f"Could you expand on {point}?"

    async def generate_final_report(self, summary: str, language: str) -> str:
        return summary
