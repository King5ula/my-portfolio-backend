import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.rate_limit import chat_limiter, contact_limiter
from app.schemas.contact import ContactRequest
from app.services.chat_backend import MockChatBackend, get_chat_backend
from app.services.email import get_email_sender


class FakeEmailSender:
    def __init__(self) -> None:
        self.sent: list[ContactRequest] = []

    async def send_contact_email(self, contact: ContactRequest) -> None:
        self.sent.append(contact)


@pytest.fixture
def email_sender() -> FakeEmailSender:
    return FakeEmailSender()


@pytest.fixture
def client(email_sender: FakeEmailSender):
    # Overrides keep every test offline, whatever the local .env says.
    app.dependency_overrides[get_chat_backend] = lambda: MockChatBackend()
    app.dependency_overrides[get_email_sender] = lambda: email_sender
    chat_limiter.reset()
    contact_limiter.reset()
    yield TestClient(app)
    app.dependency_overrides.clear()
