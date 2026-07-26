"""
Execution Plan Validator.
"""

from platformmind.application.planner.validators.guardrails import PolicyEngine
from platformmind.domain.models.execution import ExecutionPlan


class ExecutionPlanValidator:
    """
    Validates an ExecutionPlan before it leaves the planner.
    Enforces strict security guardrails on the final plan.
    """

    def validate(self, plan: ExecutionPlan) -> bool:
        if getattr(plan, "risk_score", 0.0) >= 1.0:
            return (
                False  # Risk score is intolerably high (e.g. forbidden tools present)
            )

        for step in plan.steps:
            if not PolicyEngine.is_tool_allowed(step.tool_name):
                return False  # Strictly forbidden tool

        return True
