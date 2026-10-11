import logging
import re

from fastapi import APIRouter, Depends, HTTPException

from app.rate_limit import chat_limiter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_backend import ChatBackend, ChatBackendError, get_chat_backend

logger = logging.getLogger(__name__)

router = APIRouter()

_EMPHASIS = re.compile(r"(\*\*|__|\*|`)(\S(?:.*?\S)?)\1", re.DOTALL)
_LINE_PREFIX = re.compile(r"^\s{0,3}(#{1,6}\s+|[-*]\s+)", re.MULTILINE)


def to_plain_text(reply: str) -> str:
    """The chat widget shows text as-is, so markdown markers would appear literally."""
    return _EMPHASIS.sub(r"\2", _LINE_PREFIX.sub("", reply)).strip()


@router.post("/chat", response_model=ChatResponse, dependencies=[Depends(chat_limiter)])
async def chat(
    body: ChatRequest, backend: ChatBackend = Depends(get_chat_backend)
) -> ChatResponse:
    try:
        reply = await backend.reply(body.user_message)
    except ChatBackendError:
        # Logged in full here; the visitor only gets a generic message.
        logger.exception("Chat backend failed")
        raise HTTPException(
            status_code=502,
            detail="David's AI clone is unavailable right now. Please try again shortly.",
        )
    return ChatResponse(reply=to_plain_text(reply))
