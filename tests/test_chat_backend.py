import json

import httpx
import pytest

from app.config import Settings
from app.prompts.david_prompt import DAVID_PROMPT
from app.services.chat_backend import (
    ChatBackendError,
    MockChatBackend,
    OpenRouterChatBackend,
    build_chat_backend,
)


def _backend(handler, models=("model-a", "model-b")) -> OpenRouterChatBackend:
    return OpenRouterChatBackend(
        "test-key", list(models), transport=httpx.MockTransport(handler)
    )


def _ok(text: str) -> httpx.Response:
    return httpx.Response(200, json={"choices": [{"message": {"content": text}}]})


async def test_sends_persona_prompt_and_user_message():
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return _ok("Kia ora")

    reply = await _backend(handler).reply("Who are you?")

    assert reply == "Kia ora"
    assert len(seen) == 1
    assert seen[0].headers["Authorization"] == "Bearer test-key"
    body = json.loads(seen[0].content)
    assert body["model"] == "model-a"
    assert body["messages"] == [
        {"role": "system", "content": DAVID_PROMPT},
        {"role": "user", "content": "Who are you?"},
    ]


async def test_falls_back_to_next_model():
    tried: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        model = json.loads(request.content)["model"]
        tried.append(model)
        if model == "model-a":
            return httpx.Response(429, json={"error": "rate limited"})
        return _ok("from b")

    assert await _backend(handler).reply("hi") == "from b"
    assert tried == ["model-a", "model-b"]


async def test_empty_or_malformed_response_counts_as_failure():
    responses = iter([httpx.Response(200, json={"choices": []}), _ok("")])

    with pytest.raises(ChatBackendError):
        await _backend(lambda request: next(responses)).reply("hi")


async def test_network_error_on_every_model_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no network")

    with pytest.raises(ChatBackendError, match="All OpenRouter models failed"):
        await _backend(handler).reply("hi")


def test_build_selects_backend_from_settings():
    mock = Settings(_env_file=None, llm_backend="mock")
    real = Settings(_env_file=None, llm_backend="openrouter", openrouter_api_key="k")
    missing_key = Settings(_env_file=None, llm_backend="openrouter", openrouter_api_key="")

    assert isinstance(build_chat_backend(mock), MockChatBackend)
    assert isinstance(build_chat_backend(real), OpenRouterChatBackend)
    with pytest.raises(RuntimeError, match="OPENROUTER_API_KEY"):
        build_chat_backend(missing_key)


def test_model_list_is_parsed_from_comma_separated_setting():
    settings = Settings(_env_file=None, openrouter_models=" a , b,, c ")

    assert settings.openrouter_model_list == ["a", "b", "c"]
