"""
Execution Domain Models.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from platformmind.core.utils.clock import Clock
from platformmind.domain.enums import ExecutionStatus, ExecutionStepStatus
from platformmind.domain.value_objects import (
    ExecutionDuration,
    ExecutionId,
    InstructionId,
)


class ExecutionStep(BaseModel):
    """
    Represents one executable step.
    """

    step_id: str
    name: str
    description: str
    tool_name: str
    title: str = ""
    tool_reason: str = ""
    inputs: dict[str, Any] = Field(default_factory=dict)
    outputs: dict[str, Any] = Field(default_factory=dict)
    expected_outputs: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    status: ExecutionStepStatus = Field(default=ExecutionStepStatus.PENDING)
    retry_count: int = Field(default=0)
    estimated_duration: float = 0.5
    retry_policy: dict[str, Any] = Field(
        default_factory=lambda: {"max_retries": 3, "backoff": "exponential"}
    )
    rollback_supported: bool = True
    confidence: float = 1.0
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=False)


class ExecutionPlan(BaseModel):
    """
    Represents an ordered execution plan.
    """

    plan_id: ExecutionId = Field(default_factory=ExecutionId)
    instruction_id: InstructionId
    instruction_text: str = ""
    detected_intent: str = "issue_management"
    complexity: str = "MODERATE"
    reasoning: str = "Autonomous task decomposition based on intent classification and tool matching."
    selected_tools: list[str] = Field(default_factory=list)
    alternative_tools: list[str] = Field(default_factory=list)
    estimated_duration: float = 1.2
    estimated_api_calls: int = 2
    memory_matches: int = 1
    decomposition_strategy: str = "sequential_dependency"

    # New Explainability and Metrics fields
    expected_success_rate: float = 0.0
    risk_score: float = 0.0
    memory_match_percent: float = 0.0
    capability_match_percent: float = 0.0
    constraint_count: int = 0
    learning_influence_percent: float = 0.0
    planner_confidence: float = 0.0
    alternative_plans_considered: list[str] = Field(default_factory=list)
    why_this_plan: str = ""

    steps: list[ExecutionStep] = Field(default_factory=list)
    estimated_cost: float = Field(default=0.0)
    estimated_time: ExecutionDuration = Field(
        default_factory=lambda: ExecutionDuration(seconds=0.0)
    )  # noqa: E501
    confidence: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=Clock.now)

    def add_step(self, step: ExecutionStep) -> None:
        self.steps.append(step)

    def remove_step(self, step_id: str) -> None:
        self.steps = [s for s in self.steps if s.step_id != step_id]

    def reorder_steps(self, step_ids: list[str]) -> None:
        step_map = {s.step_id: s for s in self.steps}
        if set(step_ids) != set(step_map.keys()):
            raise ValueError("All current step IDs must be provided for reordering.")
        self.steps = [step_map[sid] for sid in step_ids]

    def validate_dependencies(self) -> bool:
        available: set[str] = set()
        for step in self.steps:
            for dep in step.dependencies:
                if dep not in available:
                    return False
            available.add(step.step_id)
        return True

    def total_steps(self) -> int:
        return len(self.steps)


class ExecutionState(BaseModel):
    """
    Represents runtime execution state.
    """

    current_step: str | None = None
    completed_steps: list[str] = Field(default_factory=list)
    failed_steps: list[str] = Field(default_factory=list)
    status: ExecutionStatus = Field(default=ExecutionStatus.PENDING)

    @property
    def progress_percentage(self) -> float:
        total = len(self.completed_steps) + len(self.failed_steps)
        if total == 0 and not self.current_step:
            return 0.0
        # In a real scenario we'd need total steps from the plan,
        # but this is a simplified view of state.
        return 0.0


class ExecutionResult(BaseModel):
    """
    Represents final execution outcome.
    """

    execution_id: ExecutionId
    status: ExecutionStatus
    outputs: dict[str, Any] = Field(default_factory=dict)
    execution_time: ExecutionDuration
    api_calls: int = Field(default=0)
    retries: int = Field(default=0)
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    traces: list[dict[str, Any]] = Field(default_factory=list)
    completed_steps: list[str] = Field(default_factory=list)
    failed_steps: list[str] = Field(default_factory=list)
    skipped_steps: list[str] = Field(default_factory=list)
    final_output: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)
