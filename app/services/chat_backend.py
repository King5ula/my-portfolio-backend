import logging
from functools import lru_cache
from typing import Protocol

import httpx

from app.config import Settings, get_settings
from app.prompts.david_prompt import DAVID_PROMPT

logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class ChatBackendError(Exception):
    """The backend could not produce a reply."""


class ChatBackend(Protocol):
    async def reply(self, user_message: str) -> str: ...


class MockChatBackend:
    """Canned reply, no network call. Selected with LLM_BACKEND=mock."""

    async def reply(self, user_message: str) -> str:
        return (
            "Hi, I'm David's AI clone running in mock mode, so this is a canned "
            "reply. Set LLM_BACKEND=openrouter to talk to a real model."
        )


class OpenRouterChatBackend:
    def __init__(
        self,
        api_key: str,
        models: list[str],
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._api_key = api_key
        self._models = models
        self._transport = transport

    async def reply(self, user_message: str) -> str:
        last_error: Exception | None = None
        async with httpx.AsyncClient(timeout=30, transport=self._transport) as client:
            for model in self._models:
                try:
                    return await self._call(client, model, user_message)
                except (httpx.HTTPError, ChatBackendError) as exc:
                    logger.warning("Model %s failed: %s", model, exc)
                    last_error = exc
        raise ChatBackendError("All OpenRouter models failed") from last_error

    async def _call(
        self, client: httpx.AsyncClient, model: str, user_message: str
    ) -> str:
        response = await client.post(
            OPENROUTER_URL,
            headers={"Authorization": f"Bearer {self._api_key}"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": DAVID_PROMPT},
                    {"role": "user", "content": user_message},
                ],
            },
        )
        if response.status_code >= 400:
            raise ChatBackendError(
                f"OpenRouter API ({response.status_code}): {response.text[:200]}"
            )
        try:
            content = response.json()["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise ChatBackendError("No text in response") from exc
        if not content:
            raise ChatBackendError("No text in response")
        return content


def build_chat_backend(settings: Settings) -> ChatBackend:
    if settings.llm_backend == "mock":
        return MockChatBackend()
    if not settings.openrouter_api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Set it, or set LLM_BACKEND=mock."
        )
    return OpenRouterChatBackend(
        settings.openrouter_api_key, settings.openrouter_model_list
    )


@lru_cache
def get_chat_backend() -> ChatBackend:
    return build_chat_backend(get_settings())
