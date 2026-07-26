"""
Metrics Router.
"""

import inspect
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Request

from platformmind.api.dependencies import get_metrics_engine
from platformmind.api.schemas.responses import APIResponse, MetricResponse

router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.get(
    "",
    response_model=APIResponse[MetricResponse],
    summary="Retrieve Agent Performance Metrics",
    description="""
    Calculates and returns key performance indicators for the autonomous agent.
    Metrics cover execution time, API call efficiency, learning improvements, and planner accuracy over time.
    """,
)
async def get_metrics(
    request: Request, engine=Depends(get_metrics_engine)
) -> APIResponse[MetricResponse]:
    req_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    raw_metrics = {}
    if hasattr(engine, "get_metrics"):
        res = engine.get_metrics()
        raw_metrics = await res if inspect.isawaitable(res) else res

    data = MetricResponse(
        total_executions=raw_metrics.get("total_executions", 0),
        successful_executions=raw_metrics.get("successful_executions", 0),
        failed_executions=raw_metrics.get("failed_executions", 0),
        average_execution_time=raw_metrics.get("average_execution_time", 0.0),
        average_api_calls=raw_metrics.get("average_api_calls", 0.0),
        retry_rate=raw_metrics.get("retry_rate", 0.0),
        rollback_rate=raw_metrics.get("rollback_rate", 0.0),
        capability_reuse_rate=raw_metrics.get("capability_reuse_rate", 0.0),
        capability_synthesis_count=raw_metrics.get("capability_synthesis_count", 0),
        capability_synthesis_rate=raw_metrics.get("capability_synthesis_rate", 0.0),
        planner_accuracy=raw_metrics.get("planner_accuracy", 1.0),
        memory_hit_rate=raw_metrics.get("memory_hit_rate", 1.0),
        constraint_discovery_count=raw_metrics.get("constraint_discovery_count", 0),
        learning_improvement=raw_metrics.get("time_improvement_pct", 0.0),
        execution_improvement=raw_metrics.get("calls_improvement_pct", 0.0),
        memory_size=raw_metrics.get("memory_size", 0),
        constraints_learned=raw_metrics.get("constraints_learned", 0),
        success_trend=raw_metrics.get("success_trend", []),
        execution_trend=raw_metrics.get("execution_trend", []),
        api_call_trend=raw_metrics.get("api_call_trend", []),
        time_trend=raw_metrics.get("time_trend", []),
        tool_usage=raw_metrics.get("tool_usage", {}),
        most_common_instruction=raw_metrics.get("most_common_instruction", None),
        most_used_capability=raw_metrics.get("most_used_capability", None),
    )

    return APIResponse(
        status="success", data=data, request_id=req_id, timestamp=datetime.utcnow()
    )
