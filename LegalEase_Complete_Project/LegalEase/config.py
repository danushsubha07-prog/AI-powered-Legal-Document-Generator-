from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LegalEase - AI Legal Document Generator"
    app_version: str = "1.0.0"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    frontend_api_url: str = "http://127.0.0.1:8000"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.8-flash"
    demo_mode: bool = True

    max_input_chars: int = 30000
    max_output_tokens: int = 12000
    temperature: float = 0.35
    request_timeout_seconds: int = 120

    company_name: str = "LegalEase"
    company_tagline: str = "AI-Powered Legal Document Generator"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
