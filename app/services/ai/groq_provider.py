import httpx

from app.config import settings
from app.services.ai.base import AIContext, BaseAIProvider, build_evaluation_prompt, parse_ai_evaluation


class GroqProvider(BaseAIProvider):
    name = "groq"

    async def evaluate_answer(self, context: AIContext):
        async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.groq_api_key}"},
                json={
                    "model": settings.groq_model or "llama-3.1-8b-instant",
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
        return f"Could you explain {point} in more detail?"

    async def generate_final_report(self, summary: str, language: str) -> str:
        return summary
