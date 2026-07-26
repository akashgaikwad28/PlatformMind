"""
Sandbox Tester.
"""

from platformmind.domain.models.execution import ExecutionPlan


class SandboxTester:
    """
    Simulates execution to verify the generated capability.
    """

    async def test(self, plan: ExecutionPlan) -> bool:
        """
        In a real system, this executes the plan in dry-run mode.
        """
        # Simulate successful validation
        return True
