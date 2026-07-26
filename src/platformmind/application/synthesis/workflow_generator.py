"""
Workflow Generator.
"""

import uuid
from typing import Any

from platformmind.domain.models.execution import ExecutionPlan, ExecutionStep
from platformmind.domain.value_objects import ExecutionId, InstructionId


class WorkflowGenerator:
    """
    Generates a reusable ExecutionPlan template for the capability.
    """

    def generate(self, design: dict[str, Any]) -> ExecutionPlan:
        steps = []
        for i, tool_name in enumerate(design.get("required_tools", [])):
            steps.append(
                ExecutionStep(
                    step_id=f"step_{i + 1}",
                    name=f"Execute {tool_name}",
                    description=f"Synthesized step {i + 1}",
                    tool_name=tool_name,
                    dependencies=[f"step_{i}"] if i > 0 else [],
                )
            )

        return ExecutionPlan(
            plan_id=ExecutionId(value=f"template_{uuid.uuid4().hex[:8]}"),
            instruction_id=InstructionId(value="template"),
            steps=steps,
        )
