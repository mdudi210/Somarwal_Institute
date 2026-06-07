from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Somarwal Institute API"
    secret_key: str = "dev-secret-change-me"
    algorithm: str = "HS256"
    database_url: str = "sqlite:///./somarwal.db"
    access_token_minutes: int = 15
    refresh_token_days: int = 7
    allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
