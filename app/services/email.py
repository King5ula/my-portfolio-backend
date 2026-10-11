import asyncio
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from functools import lru_cache
from html import escape
from typing import Protocol

import httpx

from app.config import Settings, get_settings
from app.schemas.contact import ContactRequest

RESEND_URL = "https://api.resend.com/emails"


class EmailSender(Protocol):
    async def send_contact_email(self, contact: ContactRequest) -> None: ...


class EmailSendError(Exception):
    """The email provider rejected or could not accept the message."""


@dataclass
class ContactEmail:
    subject: str
    text: str
    html: str


def build_contact_email(contact: ContactRequest) -> ContactEmail:
    # The visitor's input is escaped so it can't inject markup into the email.
    name, email, body = escape(contact.name), escape(contact.email), escape(contact.message)
    return ContactEmail(
        subject=f"💼 New Portfolio Message from {contact.name}",
        text=(
            "You received a message via your portfolio site contact form:\n\n"
            f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}"
        ),
        html=f"""
      <div style="font-family: sans-serif; padding: 20px; color: #333;">
        <h2 style="color: #4f46e5; border-bottom: 1px solid #ddd; padding-bottom: 10px;">New Portfolio Contact</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
        <div style="background: #f9f9f9; padding: 15px; border-radius: 8px; margin-top: 15px; border-left: 4px solid #4f46e5;">
          <p style="white-space: pre-wrap; margin: 0;">{body}</p>
        </div>
      </div>
    """,
    )


def build_contact_message(contact: ContactRequest, settings: Settings) -> EmailMessage:
    content = build_contact_email(contact)
    message = EmailMessage()
    message["From"] = f'"Portfolio Contact" <{settings.email_user}>'
    message["To"] = settings.email_receiver
    message["Reply-To"] = contact.email
    message["Subject"] = content.subject
    message.set_content(content.text)
    message.add_alternative(content.html, subtype="html")
    return message


class SmtpEmailSender:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def send_contact_email(self, contact: ContactRequest) -> None:
        message = build_contact_message(contact, self._settings)
        # smtplib is blocking, so it runs off the event loop.
        await asyncio.to_thread(self._send, message)

    def _send(self, message: EmailMessage) -> None:
        settings = self._settings
        with smtplib.SMTP_SSL(settings.email_host, settings.email_port, timeout=30) as smtp:
            smtp.login(settings.email_user, settings.email_pass)
            smtp.send_message(message)


class ResendEmailSender:
    """Sends through Resend's HTTPS API, for hosts that block SMTP ports."""

    def __init__(
        self, settings: Settings, transport: httpx.AsyncBaseTransport | None = None
    ) -> None:
        self._settings = settings
        self._transport = transport

    async def send_contact_email(self, contact: ContactRequest) -> None:
        content = build_contact_email(contact)
        settings = self._settings
        async with httpx.AsyncClient(timeout=30, transport=self._transport) as client:
            response = await client.post(
                RESEND_URL,
                headers={"Authorization": f"Bearer {settings.resend_api_key}"},
                json={
                    "from": settings.resend_from,
                    "to": [settings.email_receiver],
                    "reply_to": contact.email,
                    "subject": content.subject,
                    "text": content.text,
                    "html": content.html,
                },
            )
        if response.status_code >= 400:
            raise EmailSendError(f"Resend API ({response.status_code}): {response.text[:200]}")


def build_email_sender(settings: Settings) -> EmailSender:
    if settings.resend_api_key:
        return ResendEmailSender(settings)
    return SmtpEmailSender(settings)


@lru_cache
def get_email_sender() -> EmailSender:
    return build_email_sender(get_settings())
