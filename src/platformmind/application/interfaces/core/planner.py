"""
Planner Interface.
"""

from abc import ABC, abstractmethod

from platformmind.domain.models.execution import ExecutionPlan
from platformmind.domain.models.instruction import Instruction


class Planner(ABC):
    """
    Contract for generating execution plans from instructions.
    """

    @abstractmethod
    async def plan(
        self, instruction: Instruction, previous_results: list = None
    ) -> ExecutionPlan:
        pass
