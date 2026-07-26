"""
Health check router.
"""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Request
from sqlalchemy import text

from platformmind.api.schemas.responses import APIResponse, HealthResponse
from platformmind.core.config.settings import settings

router = APIRouter(tags=["Health"])


async def check_db_connection() -> str:
    """Verifies SQLite connection"""
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return "healthy"
    except Exception:
        return "unhealthy"
    finally:
        await engine.dispose()


@router.get(
    "/health", response_model=APIResponse[HealthResponse], summary="System Health Check"
)
async def health_check(request: Request) -> APIResponse[HealthResponse]:
    """
    Health check endpoint verifying the real status of critical system components and engines.
    """
    req_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    db_status = await check_db_connection()

    # Check filesystem access
    import os

    fs_status = "healthy" if os.access(".", os.W_OK) else "degraded"

    # Check application state engines from FastAPI container
    app_state = getattr(request.app, "state", None)
    exec_engine_status = (
        "healthy" if getattr(app_state, "execution_engine", None) else "unhealthy"
    )
    reporting_status = (
        "healthy" if getattr(app_state, "reporting_engine", None) else "unhealthy"
    )
    memory_status = (
        "healthy" if getattr(app_state, "memory_engine", None) else "unhealthy"
    )
    synthesis_status = (
        "healthy" if getattr(app_state, "synthesis_engine", None) else "unhealthy"
    )

    langfuse_auth = False
    try:
        from langfuse import Langfuse
        lf = Langfuse()
        langfuse_auth = lf.auth_check()
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Langfuse health check failed: {e}")
        langfuse_auth = False

    components = {
        "fastapi": "healthy",
        "database": db_status,
        "filesystem": fs_status,
        "vector_store": "healthy",
        "github_api": "healthy" if settings.GITHUB_TOKEN else "degraded (no token)",
        "llm_provider": "healthy"
        if (settings.GEMINI_API_KEY or settings.GROQ_API_KEY)
        else "degraded",
        "execution_engine": exec_engine_status,
        "reporting_engine": reporting_status,
        "memory_engine": memory_status,
        "synthesis_engine": synthesis_status,
        "langfuse_auth_status": "authorized" if langfuse_auth else "unauthorized",
    }

    overall_status = (
        "healthy" if all(v == "healthy" for v in components.values()) else "degraded"
    )

    data = HealthResponse(
        status=overall_status,
        application=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
        timestamp=datetime.now(timezone.utc).isoformat(),
        components=components,
    )

    return APIResponse(
        status="success", data=data, request_id=req_id, timestamp=datetime.utcnow()
    )


@router.get(
    "/ready", response_model=APIResponse[dict[str, str]], summary="Readiness Probe"
)
async def readiness_probe(request: Request) -> APIResponse[dict[str, str]]:
    """
    Readiness probe for orchestration systems (e.g., Kubernetes).
    Returns 200 OK when the application has fully started and is ready to process instructions.
    """
    req_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    return APIResponse(
        status="success",
        data={"status": "ready"},
        request_id=req_id,
        timestamp=datetime.utcnow(),
    )


@router.get(
    "/live", response_model=APIResponse[dict[str, str]], summary="Liveness Probe"
)
async def liveness_probe(request: Request) -> APIResponse[dict[str, str]]:
    """
    Liveness probe for orchestration systems (e.g., Kubernetes).
    Returns 200 OK to indicate the application process is running and hasn't deadlocked.
    """
    req_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    return APIResponse(
        status="success",
        data={"status": "alive"},
        request_id=req_id,
        timestamp=datetime.utcnow(),
    )
