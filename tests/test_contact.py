from app.config import Settings
from app.main import app
from app.schemas.contact import ContactRequest
from app.services.email import build_contact_message, get_email_sender

VALID = {"name": "Ada", "email": "ada@example.com", "message": "Hello David"}


class FailingEmailSender:
    async def send_contact_email(self, contact: ContactRequest) -> None:
        raise OSError("smtp down")


def test_contact_sends_email(client, email_sender):
    response = client.post("/api/contact", json=VALID)

    assert response.status_code == 200
    assert response.json() == {"success": "Your message has been delivered successfully!"}
    assert [c.model_dump() for c in email_sender.sent] == [VALID]


def test_contact_requires_all_fields(client, email_sender):
    for missing in VALID:
        body = {key: value for key, value in VALID.items() if key != missing}

        response = client.post("/api/contact", json=body)

        assert response.status_code == 400
        assert response.json() == {"error": "All contact fields are required."}
    assert email_sender.sent == []


def test_contact_rejects_invalid_email(client, email_sender):
    response = client.post("/api/contact", json={**VALID, "email": "not-an-email"})

    assert response.status_code == 400
    assert response.json() == {"error": "Please enter a valid email address."}
    assert email_sender.sent == []


def test_contact_send_failure_returns_500(client):
    app.dependency_overrides[get_email_sender] = lambda: FailingEmailSender()

    response = client.post("/api/contact", json=VALID)

    assert response.status_code == 500
    assert response.json() == {
        "error": "Failed to forward your message. Please try again later."
    }


def test_contact_is_rate_limited(client):
    for _ in range(5):
        assert client.post("/api/contact", json=VALID).status_code == 200

    assert client.post("/api/contact", json=VALID).status_code == 429


def test_contact_email_escapes_visitor_html():
    settings = Settings(
        _env_file=None, email_user="me@example.com", email_receiver="me@example.com"
    )
    contact = ContactRequest(
        name="<b>Ada</b>", email="ada@example.com", message="<script>alert(1)</script>"
    )

    message = build_contact_message(contact, settings)
    html = message.get_body(preferencelist=("html",)).get_content()
    text = message.get_body(preferencelist=("plain",)).get_content()

    assert "<script>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "<script>alert(1)</script>" in text
    assert message["Reply-To"] == "ada@example.com"
    assert message["To"] == "me@example.com"
