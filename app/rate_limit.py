import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request


class RateLimiter:
    """In-memory sliding-window limit per client IP, used as a route dependency.

    State lives in this process only, which suits a single-instance deployment.
    """

    def __init__(self, max_requests: int, window_seconds: float, message: str) -> None:
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._message = message
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def __call__(self, request: Request) -> None:
        client = request.client.host if request.client else "unknown"
        now = time.monotonic()
        hits = self._hits[client]
        while hits and now - hits[0] >= self._window_seconds:
            hits.popleft()
        if len(hits) >= self._max_requests:
            raise HTTPException(status_code=429, detail=self._message)
        hits.append(now)

    def reset(self) -> None:
        self._hits.clear()


chat_limiter = RateLimiter(
    max_requests=20,
    window_seconds=120,
    message="Too many requests sent to David's AI clone. Please slow down and try again shortly.",
)

contact_limiter = RateLimiter(
    max_requests=5,
    window_seconds=15 * 60,
    message="Too many messages sent from this device. Please try again later.",
)
