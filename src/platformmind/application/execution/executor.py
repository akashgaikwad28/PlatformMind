"""
Step Executor.
"""

from platformmind.application.execution.tool_registry import ToolRegistry
from platformmind.core.telemetry.tracer import trace_step
from platformmind.domain.models.execution import ExecutionStep
from platformmind.infrastructure.github.schemas.schemas import ToolResult


class StepExecutor:
    """
    Executes a single ExecutionStep via the ToolRegistry.
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    @trace_step("StepExecutor.execute")
    async def execute(self, step: ExecutionStep) -> ToolResult:
        tool = self.registry.get(step.tool_name)

        # Execute the tool with the step inputs
        result = await tool.run(**step.inputs)
        return result
