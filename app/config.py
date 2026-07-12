from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "InterviewForge AI"
    app_env: str = "development"
    app_debug: bool = True
    app_secret_key: str = "change-me"
    app_url: str = "http://127.0.0.1:8000"

    database_url: str = "sqlite:///./interviewforge.db"

    session_cookie_name: str = "interviewforge_session"
    session_cookie_secure: bool = False
    session_expire_hours: int = 168

    ai_provider: str = "mock"
    ai_timeout_seconds: int = 45
    ai_max_retries: int = 2

    groq_api_key: str = ""
    groq_model: str = ""
    gemini_api_key: str = ""
    gemini_model: str = ""
    openrouter_api_key: str = ""
    openrouter_model: str = ""
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b"

    encryption_key: str = ""
    max_answer_length: int = 10000
    max_interview_questions: int = 20
    question_data_dir: str = "data/questions"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    @property
    def secret_key(self) -> str:
        if self.app_secret_key == "change-me" and self.is_production:
            raise ValueError("APP_SECRET_KEY must be changed in production.")
        return self.app_secret_key


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

