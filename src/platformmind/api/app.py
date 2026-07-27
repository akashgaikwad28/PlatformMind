"""
Application factory for PlatformMind.
"""

import os

# Load .env FIRST, before any other module imports.
# This ensures Langfuse (and other SDKs) find their env vars at import time.
import dotenv

dotenv.load_dotenv()

# Ensure Langfuse SDK finds the host under both env var names.
# Render has LANGFUSE_HOST set; newer Langfuse SDK versions also look for LANGFUSE_BASE_URL.
_lf_host = os.environ.get("LANGFUSE_HOST") or os.environ.get("LANGFUSE_BASE_URL")
if _lf_host:
    os.environ.setdefault("LANGFUSE_BASE_URL", _lf_host)
    os.environ.setdefault("LANGFUSE_HOST", _lf_host)

# Only enable Langfuse debug logging in development to avoid flooding production logs
if os.environ.get("APP_ENV", "development") == "development":
    os.environ["LANGFUSE_DEBUG"] = "True"

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from platformmind.api.exception_handlers import (
    global_exception_handler,
    platformmind_exception_handler,
)
from platformmind.api.middleware import (
    LoggingMiddleware,
    RequestIDMiddleware,
    TimingMiddleware,
)
from platformmind.api.routers import health
from platformmind.core.config.settings import settings
from platformmind.domain.exceptions.exceptions import PlatformMindException
from platformmind.infrastructure.logging.logger import get_logger, setup_logger

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan handler.
    """
    setup_logger()
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")

    # Wire the real dependencies!
    from platformmind.api.container import setup_container

    setup_container(app)

    yield

    # Flush and shut down Langfuse gracefully so the last batch of traces is not lost
    from platformmind.core.telemetry.langfuse_client import shutdown_langfuse

    shutdown_langfuse()

    logger.info(f"Shutting down {settings.APP_NAME}")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Autonomous Platform Intelligence Agent API",
        openapi_tags=[{"name": "Health", "description": "System health operations"}],
        lifespan=lifespan,
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(RequestIDMiddleware)

    from fastapi.exceptions import RequestValidationError

    from platformmind.api.exception_handlers import validation_exception_handler

    # Exception Handlers
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(PlatformMindException, platformmind_exception_handler)  # type: ignore  # noqa: E501
    app.add_exception_handler(Exception, global_exception_handler)

    # Routers
    app.include_router(health.router, prefix="/api")

    from platformmind.api.routers.v1.capabilities import router as capabilities_router
    from platformmind.api.routers.v1.execution import router as execution_router
    from platformmind.api.routers.v1.memory import router as memory_router
    from platformmind.api.routers.v1.metrics import router as metrics_router
    from platformmind.api.routers.v1.reports import router as reports_router
    from platformmind.api.routers.v1.synthesis import router as synthesis_router

    app.include_router(execution_router, prefix="/api/v1")
    app.include_router(memory_router, prefix="/api/v1")
    app.include_router(capabilities_router, prefix="/api/v1")
    app.include_router(reports_router, prefix="/api/v1")
    app.include_router(metrics_router, prefix="/api/v1")
    app.include_router(synthesis_router, prefix="/api/v1")

    return app
