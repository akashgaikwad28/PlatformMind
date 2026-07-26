"""
Execution Context.
"""

from dataclasses import dataclass, field
from typing import Any

from platformmind.domain.models.execution import ExecutionPlan


@dataclass
class ExecutionContext:
    """
    Immutable-style runtime context for an execution.
    """

    execution_id: str
    plan: ExecutionPlan
    shared_variables: dict[str, Any] = field(default_factory=dict)

    def copy_with_update(self, **kwargs: Any) -> "ExecutionContext":
        # Provide a way to create a new context with updated variables
        # to mimic immutability for the orchestrator.
        new_vars = dict(self.shared_variables)
        if "shared_variables" in kwargs:
            new_vars.update(kwargs.pop("shared_variables"))

        params = {
            "execution_id": self.execution_id,
            "plan": self.plan,
            "shared_variables": new_vars,
        }
        params.update(kwargs)
        return ExecutionContext(**params)
