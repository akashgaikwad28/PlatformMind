"""
Report Domain Model.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from platformmind.domain.models.execution import ExecutionPlan
from platformmind.domain.models.instruction import Instruction


class ExecutionReport(BaseModel):
    """
    Represents the structured report returned to users.
    """

    instruction: Instruction
    execution_plan: ExecutionPlan
    execution_summary: str
    metrics: dict[str, Any] = Field(default_factory=dict)
    failures: list[str] = Field(default_factory=list)
    memory_updates: list[str] = Field(default_factory=list)
    learning_updates: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)
