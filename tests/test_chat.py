from app.main import app
from app.services.chat_backend import ChatBackendError, get_chat_backend


class FailingChatBackend:
    async def reply(self, user_message: str) -> str:
        raise ChatBackendError("upstream said: secret-internal-detail")


class EchoChatBackend:
    async def reply(self, user_message: str) -> str:
        return f"echo: {user_message}"


def test_chat_returns_reply(client):
    app.dependency_overrides[get_chat_backend] = lambda: EchoChatBackend()

    response = client.post("/api/chat", json={"userMessage": "  What do you build?  "})

    assert response.status_code == 200
    assert response.json() == {"reply": "echo: What do you build?"}


def test_chat_rejects_blank_message(client):
    for body in ({}, {"userMessage": ""}, {"userMessage": "   "}):
        response = client.post("/api/chat", json=body)

        assert response.status_code == 400
        assert response.json() == {"error": "Message content cannot be blank."}


def test_chat_rejects_wrong_type(client):
    response = client.post("/api/chat", json={"userMessage": 42})

    assert response.status_code == 400
    assert response.json() == {"error": "Invalid request body."}


def test_chat_backend_failure_does_not_leak_details(client):
    app.dependency_overrides[get_chat_backend] = lambda: FailingChatBackend()

    response = client.post("/api/chat", json={"userMessage": "hello"})

    assert response.status_code == 502
    assert "secret-internal-detail" not in response.text
    assert "unavailable" in response.json()["error"]


def test_chat_is_rate_limited(client):
    for _ in range(20):
        assert client.post("/api/chat", json={"userMessage": "hi"}).status_code == 200

    response = client.post("/api/chat", json={"userMessage": "hi"})

    assert response.status_code == 429
    assert response.json()["error"].startswith("Too many requests")


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
