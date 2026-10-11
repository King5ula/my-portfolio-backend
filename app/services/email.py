import asyncio
import smtplib
from email.message import EmailMessage
from functools import lru_cache
from html import escape
from typing import Protocol

from app.config import Settings, get_settings
from app.schemas.contact import ContactRequest


class EmailSender(Protocol):
    async def send_contact_email(self, contact: ContactRequest) -> None: ...


def build_contact_message(contact: ContactRequest, settings: Settings) -> EmailMessage:
    message = EmailMessage()
    message["From"] = f'"Portfolio Contact" <{settings.email_user}>'
    message["To"] = settings.email_receiver
    message["Reply-To"] = contact.email
    message["Subject"] = f"💼 New Portfolio Message from {contact.name}"
    message.set_content(
        "You received a message via your portfolio site contact form:\n\n"
        f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}"
    )
    # The visitor's input is escaped so it can't inject markup into the email.
    name, email, body = escape(contact.name), escape(contact.email), escape(contact.message)
    message.add_alternative(
        f"""
      <div style="font-family: sans-serif; padding: 20px; color: #333;">
        <h2 style="color: #4f46e5; border-bottom: 1px solid #ddd; padding-bottom: 10px;">New Portfolio Contact</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
        <div style="background: #f9f9f9; padding: 15px; border-radius: 8px; margin-top: 15px; border-left: 4px solid #4f46e5;">
          <p style="white-space: pre-wrap; margin: 0;">{body}</p>
        </div>
      </div>
    """,
        subtype="html",
    )
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


@lru_cache
def get_email_sender() -> EmailSender:
    return SmtpEmailSender(get_settings())
