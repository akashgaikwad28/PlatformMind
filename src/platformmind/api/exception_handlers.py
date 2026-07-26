"""
Global and Custom Exception Handlers.
"""

import traceback
import uuid
from datetime import datetime

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from platformmind.api.schemas.responses import APIErrorResponse, ErrorDetail
from platformmind.domain.exceptions.exceptions import PlatformMindException
from platformmind.infrastructure.logging.logger import get_logger

logger = get_logger()


def _get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", str(uuid.uuid4()))


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    req_id = _get_request_id(request)
    details = exc.errors()

    error_detail = ErrorDetail(
        code="VALIDATION_ERROR",
        message="The request payload is invalid or malformed.",
        details=details,
        suggested_action="Review the 'details' field to correct the invalid fields in the request body.",
    )

    response_model = APIErrorResponse(
        status="error",
        error=error_detail,
        request_id=req_id,
        timestamp=datetime.utcnow(),
    )

    logger.warning(f"Validation error on {request.url.path}: {details}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response_model.model_dump(mode="json"),
    )


async def platformmind_exception_handler(
    request: Request, exc: PlatformMindException
) -> JSONResponse:
    req_id = _get_request_id(request)

    # We can inspect subclass type to set HTTP status
    # For now, default to 400 Bad Request unless it's a known internal error
    status_code = status.HTTP_400_BAD_REQUEST

    error_code = getattr(exc, "code", "PLATFORMMIND_ERROR")
    # For GitHub API failures, we might want 502 Bad Gateway
    if "GitHub" in type(exc).__name__:
        status_code = status.HTTP_502_BAD_GATEWAY
        error_code = "GITHUB_API_FAILURE"
        suggested_action = (
            "Verify repository permissions, configuration, and GitHub service status."
        )
    elif "Plan" in type(exc).__name__ or "Capability" in type(exc).__name__:
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        error_code = "PLANNER_OR_CAPABILITY_FAILURE"
        suggested_action = "Provide a simpler instruction or ensure the repository has the necessary prerequisites."
    elif "Memory" in type(exc).__name__:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = "MEMORY_FAILURE"
        suggested_action = "Retry the request. If the issue persists, the vector store may be degraded."
    else:
        suggested_action = "Verify request parameters and repository state."

    error_detail = ErrorDetail(
        code=error_code,
        message=str(exc),
        details=None,
        suggested_action=suggested_action,
    )

    response_model = APIErrorResponse(
        status="error",
        error=error_detail,
        request_id=req_id,
        timestamp=datetime.utcnow(),
    )

    logger.error(
        f"PlatformMindException during {request.method} {request.url.path}: {str(exc)}"
    )
    return JSONResponse(
        status_code=status_code,
        content=response_model.model_dump(mode="json"),
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    req_id = _get_request_id(request)

    error_detail = ErrorDetail(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred during execution.",
        details=str(exc) if request.app.debug else None,
        suggested_action="Contact system administrator or check server logs.",
    )

    response_model = APIErrorResponse(
        status="error",
        error=error_detail,
        request_id=req_id,
        timestamp=datetime.utcnow(),
    )

    logger.error(
        f"Unhandled Exception during {request.method} {request.url.path}: {str(exc)}\n{traceback.format_exc()}"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response_model.model_dump(mode="json"),
    )
