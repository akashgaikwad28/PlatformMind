"""
Execution Plan Builder.
"""

import uuid
from datetime import datetime
from typing import Any

from platformmind.domain.enums import (
    ExecutionStepStatus,
)
from platformmind.domain.models.execution import ExecutionPlan, ExecutionStep
from platformmind.domain.value_objects import ExecutionId


class ExecutionPlanBuilder:
    """
    Assembles the final validated ExecutionPlan domain model.
    """

    def build(
        self,
        instruction: str,
        normalized_instruction: str,
        intent: str,
        sorted_tasks: list[dict[str, Any]],
        tool_selection: dict[str, str],
        confidence: float,
    ) -> ExecutionPlan:
        from platformmind.domain.value_objects import InstructionId

        steps = []
        selected_tools = []
        all_alts = []

        for i, task in enumerate(sorted_tasks):
            sel = tool_selection.get(task["id"], "unknown")
            if hasattr(sel, "tool"):
                tool_name = sel.tool
                tool_reason = sel.reason
                step_conf = getattr(sel, "confidence", confidence)
                if hasattr(sel, "alternatives") and sel.alternatives:
                    all_alts.extend(sel.alternatives)
            else:
                tool_name = str(sel)
                tool_reason = f"Selected tool '{tool_name}' best matches intent '{intent}' for task action."
                step_conf = confidence

            if tool_name != "unknown" and tool_name not in selected_tools:
                selected_tools.append(tool_name)

            step = ExecutionStep(
                step_id=f"step_{i + 1}_{uuid.uuid4().hex[:8]}",
                name=task["description"],
                title=f"Step {i + 1}: {task['description'][:40]}",
                description=task["description"],
                tool_name=tool_name,
                tool_reason=tool_reason,
                inputs=task.get("inputs", {}),
                expected_outputs=["result", "status"],
                dependencies=task.get("depends_on", []),
                status=ExecutionStepStatus.PENDING,
                confidence=step_conf,
            )
            steps.append(step)

        all_tools = [
            "search_issues",
            "create_issue",
            "assign_label",
            "close_issue",
            "update_issue",
            "create_comment",
            "create_milestone",
            "get_repository",
        ]
        alt_tools = [t for t in (all_alts + all_tools) if t not in selected_tools]

        plan = ExecutionPlan(
            plan_id=ExecutionId(value=f"plan_{uuid.uuid4().hex}"),
            instruction_id=InstructionId(value=f"inst_{uuid.uuid4().hex}"),
            instruction_text=instruction,
            detected_intent=intent,
            complexity="HIGH"
            if len(steps) > 2
            else "MODERATE"
            if len(steps) > 1
            else "SIMPLE",
            reasoning=f"Decomposed instruction '{instruction}' into {len(steps)} sequential task steps based on intent '{intent}'.",
            selected_tools=selected_tools,
            alternative_tools=alt_tools[:3],
            estimated_duration=round(len(steps) * 0.6, 2),
            estimated_api_calls=len(steps),
            memory_matches=1,
            decomposition_strategy="dependency_graph_topological_sort",
            steps=steps,
            confidence=confidence,
            created_at=datetime.now(),
        )
        return plan
