"""
API Middlewares for Request ID, Timing, and Logging.
"""

import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from platformmind.infrastructure.logging.logger import get_logger

logger = get_logger()


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to inject a unique request ID into every request.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to record request timing.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log requests and responses.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = getattr(request.state, "request_id", "unknown")
        logger.info(
            f"Request started: {request.method} {request.url.path} (ID: {request_id})"
        )

        try:
            response = await call_next(request)
            logger.info(
                f"Request completed: {request.method} {request.url.path} - "
                f"Status: {response.status_code} (ID: {request_id})"
            )
            return response
        except Exception as e:
            logger.error(
                f"Request failed: {request.method} {request.url.path} - "
                f"Error: {str(e)} (ID: {request_id})"
            )
            raise
