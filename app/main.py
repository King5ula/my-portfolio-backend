import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api import chat, contact
from app.config import get_settings
from app.services.chat_backend import get_chat_backend

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Fail at startup, not on the first visitor's message, if the LLM isn't configured.
    get_chat_backend()
    if not settings.email_user or not settings.email_pass:
        logger.warning("Email credentials are blank. The contact form will fail.")
    yield


app = FastAPI(title="Portfolio Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_origin_regex=settings.cors_allowed_origin_regex or None,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
    allow_credentials=True,
)


# Every error leaves as {"error": "..."}, the shape the frontend reads.
@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    first = exc.errors()[0]
    if first.get("type") == "value_error" and "error" in first.get("ctx", {}):
        message = str(first["ctx"]["error"])
    else:
        message = "Invalid request body."
    return JSONResponse(status_code=400, content={"error": message})


app.include_router(chat.router, prefix="/api")
app.include_router(contact.router, prefix="/api")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "llm_backend": settings.llm_backend}
