from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Every env-driven setting, in one place. See .env.example."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # "mock" returns a canned reply with no network call or API key.
    llm_backend: Literal["openrouter", "mock"] = "openrouter"
    openrouter_api_key: str = ""
    # Comma-separated, tried in order until one answers.
    openrouter_models: str = (
        "nvidia/nemotron-3.5-lightning:free,"
        "liquid/lfm-2.5-2.6b:free,"
        "poolside/laguna-s-2.1:free"
    )

    email_host: str = "smtp.gmail.com"
    email_port: int = 465
    email_user: str = ""
    email_pass: str = ""
    email_receiver: str = ""

    # Comma-separated exact origins, plus one regex for Vercel preview URLs.
    cors_allowed_origins: str = "http://localhost:3000"
    cors_allowed_origin_regex: str = (
        r"^https://my-portfolio-frontend(-[a-z0-9]+)*\.vercel\.app$"
    )

    @property
    def openrouter_model_list(self) -> list[str]:
        return _split(self.openrouter_models)

    @property
    def cors_origin_list(self) -> list[str]:
        return _split(self.cors_allowed_origins)


def _split(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
