"""
Capabilities Router.
"""

import inspect
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Request

from platformmind.api.dependencies import get_capabilities_engine
from platformmind.api.schemas.responses import APIResponse, CapabilityResponse

router = APIRouter(prefix="/capabilities", tags=["Capabilities"])


@router.get(
    "",
    response_model=APIResponse[list[CapabilityResponse]],
    summary="List Agent Capabilities",
    description="""
    Returns a complete inventory of the agent's capabilities, including both pre-programmed (native) 
    and autonomously synthesized tools. Includes detailed success metrics and historical usage data.
    """,
)
async def get_capabilities(
    request: Request, engine=Depends(get_capabilities_engine)
) -> APIResponse[list[CapabilityResponse]]:
    req_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    raw_caps = []
    if hasattr(engine, "get_capabilities"):
        res = engine.get_capabilities()
        raw_caps = await res if inspect.isawaitable(res) else res

    # Map to schema
    data = []
    for cap in raw_caps:
        data.append(
            CapabilityResponse(
                id=cap.get("id", f"cap_{uuid.uuid4().hex[:8]}"),
                name=cap.get("name", "Unknown"),
                description=cap.get("description", ""),
                version=cap.get("version", "1.0.0"),
                creation_method=cap.get("creation_method", "NATIVE"),
                is_native=cap.get("is_native", True),
                creator=cap.get("creator", "SYSTEM"),
                creation_time=cap.get(
                    "creation_time",
                    cap.get("created_at", datetime.utcnow().isoformat()),
                ),
                usage_count=cap.get("usage_count", 0),
                success_rate=cap.get("success_rate", 1.0),
                failure_rate=cap.get("failure_rate", 0.0),
                average_execution_time=cap.get("average_execution_time", 0.0),
                average_api_calls=cap.get("average_api_calls", 1.0),
                confidence=cap.get("confidence", 1.0),
                created_at=cap.get("created_at", datetime.utcnow().isoformat()),
                last_used=cap.get("last_used"),
                last_updated=cap.get("last_updated", cap.get("last_used")),
                dependencies=cap.get("dependencies", []),
                constraints=cap.get("constraints", []),
                status=cap.get("status", "ACTIVE"),
            )
        )

    return APIResponse(
        status="success", data=data, request_id=req_id, timestamp=datetime.utcnow()
    )
