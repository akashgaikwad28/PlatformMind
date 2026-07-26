"""
Engine Facade.
"""

from platformmind.application.execution.orchestrator import ExecutionOrchestrator
from platformmind.domain.models.execution import ExecutionPlan, ExecutionResult


class ExecutionEngineImpl:
    """
    Primary facade for the execution engine.
    """

    def __init__(self, orchestrator: ExecutionOrchestrator):
        self.orchestrator = orchestrator

    async def execute_plan(self, plan: ExecutionPlan) -> ExecutionResult:
        return await self.orchestrator.execute(plan)
