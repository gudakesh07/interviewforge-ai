import logging

from app.config import settings
from app.services.ai.base import BaseAIProvider
from app.services.ai.gemini_provider import GeminiProvider
from app.services.ai.groq_provider import GroqProvider
from app.services.ai.mock_provider import MockAIProvider
from app.services.ai.ollama_provider import OllamaProvider
from app.services.ai.openrouter_provider import OpenRouterProvider

logger = logging.getLogger(__name__)


def get_ai_provider(name: str | None = None) -> BaseAIProvider:
    provider_name = (name or settings.ai_provider or "mock").lower()
    if provider_name == "groq" and settings.groq_api_key:
        return GroqProvider()
    if provider_name == "gemini" and settings.gemini_api_key:
        return GeminiProvider()
    if provider_name == "openrouter" and settings.openrouter_api_key:
        return OpenRouterProvider()
    if provider_name == "ollama":
        return OllamaProvider()
    logger.info("Using Mock AI provider fallback")
    return MockAIProvider()

