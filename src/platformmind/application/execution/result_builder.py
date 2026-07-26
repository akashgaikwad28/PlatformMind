"""
Result Builder.
"""

from platformmind.application.execution.metrics import ExecutionMetrics
from platformmind.application.execution.state_manager import ExecutionStateManager
from platformmind.domain.models.execution import ExecutionResult
from platformmind.domain.value_objects import ExecutionDuration, ExecutionId


class ExecutionResultBuilder:
    """
    Assembles the final ExecutionResult domain model.
    """

    def build(
        self,
        execution_id: str,
        state: ExecutionStateManager,
        metrics: ExecutionMetrics,
        outputs: dict,
        errors: list[str],
        traces: list = None,
        completed_steps: list = None,
        failed_steps: list = None,
        skipped_steps: list = None,
        final_output: dict = None,
    ) -> ExecutionResult:
        return ExecutionResult(
            execution_id=ExecutionId(value=execution_id),
            status=state.state.status,
            outputs=outputs,
            execution_time=ExecutionDuration(seconds=metrics.total_duration_seconds),
            api_calls=metrics.api_calls,
            retries=metrics.total_retries,
            errors=errors,
            warnings=[],
            traces=traces or [],
            completed_steps=completed_steps or list(state.state.completed_steps),
            failed_steps=failed_steps or list(state.state.failed_steps),
            skipped_steps=skipped_steps or [],
            final_output=final_output or {},
        )
