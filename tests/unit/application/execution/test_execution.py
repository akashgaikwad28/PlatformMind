from typing import Any
from unittest.mock import AsyncMock

import pytest

from platformmind.application.execution.executor import StepExecutor
from platformmind.application.execution.orchestrator import ExecutionOrchestrator
from platformmind.application.execution.result_builder import ExecutionResultBuilder
from platformmind.application.execution.retry import RetryManager
from platformmind.application.execution.rollback import RollbackManager
from platformmind.domain.enums import ExecutionStatus
from platformmind.domain.models.execution import ExecutionPlan, ExecutionStep
from platformmind.domain.value_objects import ExecutionId, InstructionId
from platformmind.infrastructure.github.schemas.schemas import ToolResult


@pytest.fixture
def plan() -> Any:
    return ExecutionPlan(
        plan_id=ExecutionId(value="plan-123"),
        instruction_id=InstructionId(value="inst-123"),
        steps=[
            ExecutionStep(
                step_id="step-1", name="Step 1", description="desc", tool_name="tool_1"
            ),
            ExecutionStep(
                step_id="step-2", name="Step 2", description="desc", tool_name="tool_2"
            ),
        ],
    )


@pytest.mark.asyncio
async def test_execution_orchestrator_success(plan) -> None:
    mock_executor = AsyncMock(spec=StepExecutor)
    mock_executor.execute.return_value = ToolResult(
        success=True, tool_name="test", execution_time=0.1, api_calls=1, data={"id": 1}
    )

    retry = RetryManager(max_retries=1, base_delay=0.1)
    rollback = RollbackManager()
    builder = ExecutionResultBuilder()

    orchestrator = ExecutionOrchestrator(mock_executor, retry, rollback, builder)

    result = await orchestrator.execute(plan)

    assert result.status == ExecutionStatus.COMPLETED
    assert result.api_calls == 2
    assert "step-1" in result.outputs
    assert "step-2" in result.outputs


@pytest.mark.asyncio
async def test_execution_orchestrator_failure_and_rollback(plan) -> None:
    mock_executor = AsyncMock(spec=StepExecutor)

    # Step 1 succeeds, Step 2 fails with False ToolResult
    mock_executor.execute.side_effect = [
        ToolResult(
            success=True, tool_name="t1", execution_time=0.1, api_calls=1, data={}
        ),
        ToolResult(
            success=False,
            tool_name="t2",
            execution_time=0.1,
            api_calls=1,
            errors=["Bad Request"],
        ),
    ]

    retry = RetryManager(max_retries=1, base_delay=0.1)
    rollback = RollbackManager()
    rollback.rollback = AsyncMock(return_value=True)  # Mock successful rollback

    builder = ExecutionResultBuilder()
    orchestrator = ExecutionOrchestrator(mock_executor, retry, rollback, builder)

    result = await orchestrator.execute(plan)

    # Assert execution was rolled back
    assert result.status == ExecutionStatus.CANCELLED
    assert result.api_calls == 2
    assert "step-1" in result.outputs
    assert len(result.errors) > 0
    rollback.rollback.assert_called_once()
