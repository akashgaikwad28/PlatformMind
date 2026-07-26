"""
Capability Validator.
"""

from platformmind.domain.models.execution import ExecutionPlan


class CapabilityValidator:
    """
    Validates the synthesized workflow.
    """

    def validate(self, plan: ExecutionPlan) -> bool:
        """
        Ensures the plan is structurally sound and dependencies are valid.
        """
        if not plan.steps:
            return False

        # Basic topological validation
        if not plan.validate_dependencies():
            return False

        return True
