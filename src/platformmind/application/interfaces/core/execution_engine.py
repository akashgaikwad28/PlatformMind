"""
Execution Engine Interface.
"""

from abc import ABC, abstractmethod

from platformmind.domain.models.execution import (
    ExecutionPlan,
    ExecutionResult,
    ExecutionStep,
)


class ExecutionEngine(ABC):
    """
    Contract for executing execution plans.
    """

    @abstractmethod
    async def execute(self, plan: ExecutionPlan) -> ExecutionResult:
        pass

    @abstractmethod
    async def execute_step(self, step: ExecutionStep) -> bool:
        pass

    @abstractmethod
    async def rollback(self, plan: ExecutionPlan) -> bool:
        pass

    @abstractmethod
    async def retry(self, step: ExecutionStep) -> bool:
        pass

    @abstractmethod
    async def validate(self, plan: ExecutionPlan) -> bool:
        pass
