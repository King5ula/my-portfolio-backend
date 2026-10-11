import logging

from fastapi import APIRouter, Depends, HTTPException

from app.rate_limit import contact_limiter
from app.schemas.contact import ContactRequest, ContactResponse
from app.services.email import EmailSender, get_email_sender

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/contact", response_model=ContactResponse, dependencies=[Depends(contact_limiter)]
)
async def contact(
    body: ContactRequest, sender: EmailSender = Depends(get_email_sender)
) -> ContactResponse:
    try:
        await sender.send_contact_email(body)
    except Exception:
        logger.exception("Contact email failed")
        raise HTTPException(
            status_code=500,
            detail="Failed to forward your message. Please try again later.",
        )
    return ContactResponse(success="Your message has been delivered successfully!")
