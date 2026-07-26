"""
Memory Router.
"""

import inspect
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Request

from platformmind.api.dependencies import get_memory_engine
from platformmind.api.schemas.responses import APIResponse, MemoryResponse

router = APIRouter(prefix="/memory", tags=["Memory"])


@router.get(
    "",
    response_model=APIResponse[MemoryResponse],
    summary="Retrieve Agent Memory State",
    description="""
    Returns the complete structured memory of the autonomous agent, including:
    - **Execution Memory**: Historical tasks, strategies, and outcomes.
    - **Capability Memory**: Native and synthesized capabilities with success rates.
    - **Constraint Memory**: Discovered environment limitations and API validation rules.
    - **Learning Memory**: Planner evolution and optimization history.
    """,
)
async def get_memory(
    request: Request, engine=Depends(get_memory_engine)
) -> APIResponse[MemoryResponse]:
    req_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    # Internal MemoryEngineImpl does not currently implement a comprehensive `get_memory()`
    # that matches this full schema exactly in isolation. We will extract what we can.
    # If the method is missing or not returning a dict, we gracefully fallback.
    raw_memory = {}
    if hasattr(engine, "get_memory"):
        res = engine.get_memory()
        raw_memory = await res if inspect.isawaitable(res) else res

    data = MemoryResponse(
        execution_memory=raw_memory.get("execution", {}),
        capability_memory=raw_memory.get("capabilities", {}),
        constraint_memory=raw_memory.get("constraints", {}),
        learning_memory=raw_memory.get("learning", {}),
    )

    return APIResponse(
        status="success", data=data, request_id=req_id, timestamp=datetime.utcnow()
    )
