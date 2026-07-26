"""
Planning Context Domain Models.
"""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from platformmind.domain.models.instruction import Instruction


class ExecutionMemoryContext(BaseModel):
    """Memory of previous executions."""

    previous_executions: list[dict[str, Any]] = Field(default_factory=list)
    successful_plans: list[dict[str, Any]] = Field(default_factory=list)
    failed_plans: list[dict[str, Any]] = Field(default_factory=list)
    execution_metrics: dict[str, Any] = Field(default_factory=dict)
    historical_api_calls: list[dict[str, Any]] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class CapabilityMemoryContext(BaseModel):
    """Memory of known and synthesized capabilities."""

    known_capabilities: list[str] = Field(default_factory=list)
    synthesized_capabilities: list[str] = Field(default_factory=list)
    success_rates: dict[str, float] = Field(default_factory=dict)
    usage_frequency: dict[str, int] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)


class ConstraintMemoryContext(BaseModel):
    """Memory of constraints and errors."""

    validation_errors: list[str] = Field(default_factory=list)
    permission_failures: list[str] = Field(default_factory=list)
    rate_limits: dict[str, Any] = Field(default_factory=dict)
    repository_constraints: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class LearningMemoryContext(BaseModel):
    """Memory of learned strategies and improvements."""

    best_strategies: list[str] = Field(default_factory=list)
    planner_improvements: list[str] = Field(default_factory=list)
    historical_optimization: dict[str, Any] = Field(default_factory=dict)
    tool_ranking_history: list[dict[str, Any]] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class PlanningContext(BaseModel):
    """
    The single source of truth for all execution context before planning begins.
    Used throughout the planning pipeline.
    """

    # Core Context
    instruction: Instruction
    repository: str
    repository_owner: str
    repository_name: str
    repository_type: str = Field(default="github")
    repository_permissions: dict[str, bool] = Field(default_factory=dict)

    # Execution Options
    options: dict[str, Any] = Field(default_factory=dict)
    dry_run: bool = Field(default=False)

    # Environment Context
    current_timestamp: str
    session_id: str
    previous_execution_id: Optional[str] = None
    environment: str = Field(default="production")
    llm_configuration: dict[str, Any] = Field(default_factory=dict)
    runtime_configuration: dict[str, Any] = Field(default_factory=dict)

    # Memory Contexts
    execution_memory: Optional[ExecutionMemoryContext] = None
    capability_memory: Optional[CapabilityMemoryContext] = None
    constraint_memory: Optional[ConstraintMemoryContext] = None
    learning_memory: Optional[LearningMemoryContext] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
