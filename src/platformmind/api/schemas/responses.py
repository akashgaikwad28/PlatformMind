"""
API Response Schemas.
"""

from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Error code indicating the type of failure")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Any] = Field(
        None, description="Additional context or validation errors"
    )
    suggested_action: Optional[str] = Field(
        None, description="Action the user can take to resolve the issue"
    )


class APIErrorResponse(BaseModel):
    status: str = Field(
        default="error", description="Always 'error' for failure responses"
    )
    error: ErrorDetail = Field(..., description="Detailed error information")
    request_id: str = Field(..., description="Unique trace ID for the request")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Time the error occurred"
    )


class APIResponse(BaseModel, Generic[T]):
    status: str = Field(
        default="success", description="Indicates the request was successful"
    )
    data: T = Field(..., description="The response payload")
    metadata: Optional[dict[str, Any]] = Field(
        None, description="Optional pagination or extra metadata"
    )
    request_id: str = Field(..., description="Unique trace ID for the request")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Time the response was generated"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "success",
                "data": {"key": "value"},
                "metadata": {"page": 1},
                "request_id": "req-12345",
                "timestamp": "2026-07-25T10:00:00Z",
            }
        }
    )


class HealthResponse(BaseModel):
    status: str = Field(
        ..., description="Overall system status (healthy/unhealthy/degraded)"
    )
    application: str = Field(..., description="Application name")
    version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Deployment environment")
    startup_time: Optional[str] = Field(None, description="System startup timestamp")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    components: dict[str, Any] = Field(
        ...,
        description="Status of individual subsystems (db, vector_store, github, llm, engines)",
    )


class MetricResponse(BaseModel):
    total_executions: int
    successful_executions: int
    failed_executions: int
    average_execution_time: float
    average_api_calls: float
    retry_rate: float
    rollback_rate: float = 0.0
    capability_reuse_rate: float
    capability_synthesis_count: int
    capability_synthesis_rate: float = 0.0
    planner_accuracy: float
    memory_hit_rate: float = 1.0
    constraint_discovery_count: int = 0
    learning_improvement: float
    execution_improvement: float
    memory_size: int
    constraints_learned: int
    success_trend: list[float]
    execution_trend: list[float] = []
    api_call_trend: list[float] = []
    time_trend: list[float] = []
    tool_usage: dict[str, int]
    most_common_instruction: Optional[str] = None
    most_used_capability: Optional[str] = None


class CapabilityResponse(BaseModel):
    id: str
    name: str
    description: str
    version: str
    creation_method: str
    is_native: bool
    creator: str = "SYSTEM"
    creation_time: Optional[str] = None
    usage_count: int
    success_rate: float
    failure_rate: float = 0.0
    average_execution_time: float
    average_api_calls: float = 1.0
    confidence: float
    created_at: str
    last_used: Optional[str] = None
    last_updated: Optional[str] = None
    dependencies: list[str]
    constraints: list[str] = []
    status: str


class ExecutionReportResponse(BaseModel):
    execution_id: str
    instruction: str
    planner: dict[str, Any]
    execution_plan: list[dict[str, Any]]
    execution_steps: list[dict[str, Any]]
    execution_status: str
    completed_steps: list[str]
    failed_steps: list[str]
    cancelled_steps: list[str] = []
    skipped_steps: list[str] = []
    retry_count: int
    execution_duration: float
    api_calls: int
    memory_retrieved: dict[str, Any]
    memory_updated: dict[str, Any]
    memory_before: Optional[dict[str, Any]] = None
    memory_after: Optional[dict[str, Any]] = None
    memory_delta: Optional[dict[str, Any]] = None
    capabilities_used: list[str]
    capabilities_synthesized: list[str]
    learning_updates: dict[str, Any]
    constraints_discovered: list[str]
    confidence_score: float
    warnings: list[str]
    errors: list[str]
    report_id: str
    metrics: dict[str, Any]
    final_output: Optional[dict[str, Any]] = None
    timestamps: dict[str, str]


class SynthesisHistoryResponse(BaseModel):
    id: str
    capability_gap: str
    reasoning: str
    generated_workflow: dict[str, Any]
    validation_steps: list[str]
    registered: bool
    creation_time: str
    status: str
    reuse_count: int = 0


class MemoryResponse(BaseModel):
    execution_memory: dict[str, Any] = Field(
        ..., description="Previous executions, strategies, and history"
    )
    capability_memory: dict[str, Any] = Field(
        ..., description="Known and synthesized capabilities with success rates"
    )
    constraint_memory: dict[str, Any] = Field(
        ..., description="Validation rules, limitations, and restrictions"
    )
    learning_memory: dict[str, Any] = Field(
        ..., description="Improvements, optimization history, and planner evolution"
    )
