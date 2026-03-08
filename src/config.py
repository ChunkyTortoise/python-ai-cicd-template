"""Application configuration via environment variables."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Your Service"
    environment: str = "development"
    debug: bool = False
    anthropic_api_key: str = ""
    model_name: str = "claude-sonnet-4-6"
    max_tokens: int = 1024


settings = Settings()
