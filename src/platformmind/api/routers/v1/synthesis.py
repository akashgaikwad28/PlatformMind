"""
Capability Synthesis Router.
"""

import uuid
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, Request

from platformmind.api.dependencies import get_synthesis_engine
from platformmind.api.schemas.responses import APIResponse, SynthesisHistoryResponse

router = APIRouter(prefix="/synthesis", tags=["Synthesis"])


@router.get(
    "/history",
    response_model=APIResponse[list[SynthesisHistoryResponse]],
    summary="Capability Synthesis History",
)
async def get_synthesis_history(
    request: Request, synthesis_engine: Any = Depends(get_synthesis_engine)
) -> APIResponse[list[SynthesisHistoryResponse]]:
    """
    Retrieves the complete audit history of runtime capability synthesis events.
    Includes capability gaps, reasoning, generated workflows, validation steps, and registration status.
    """
    req_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    history_data = []
    if synthesis_engine and hasattr(synthesis_engine, "get_synthesis_history"):
        history_data = synthesis_engine.get_synthesis_history()

    return APIResponse(
        status="success",
        data=history_data,
        request_id=req_id,
        timestamp=datetime.utcnow(),
    )
