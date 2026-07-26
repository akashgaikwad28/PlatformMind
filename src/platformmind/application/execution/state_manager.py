"""
State Manager.
"""

from platformmind.domain.enums import ExecutionStatus
from platformmind.domain.models.execution import ExecutionState


class ExecutionStateManager:
    """
    Manages state transitions for an execution.
    """

    def __init__(self) -> None:
        self.state = ExecutionState()

    def start_execution(self) -> None:
        self.state.status = ExecutionStatus.IN_PROGRESS

    def complete_execution(self) -> None:
        self.state.status = ExecutionStatus.COMPLETED

    def fail_execution(self) -> None:
        self.state.status = ExecutionStatus.FAILED

    def rollback_execution(self) -> None:
        self.state.status = ExecutionStatus.CANCELLED

    def start_step(self, step_id: str) -> None:
        self.state.current_step = step_id

    def complete_step(self, step_id: str) -> None:
        if step_id not in self.state.completed_steps:
            self.state.completed_steps.append(step_id)
        self.state.current_step = None

    def fail_step(self, step_id: str) -> None:
        if step_id not in self.state.failed_steps:
            self.state.failed_steps.append(step_id)
        self.state.current_step = None
