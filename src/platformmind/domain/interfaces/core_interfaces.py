"""
Core Domain Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any

from platformmind.domain.models.execution import (
    ExecutionPlan,
    ExecutionResult,
    ExecutionState,
)
from platformmind.domain.models.instruction import Instruction
from platformmind.domain.models.report import ExecutionReport


class Planner(ABC):
    @abstractmethod
    def create_plan(self, instruction: Instruction) -> ExecutionPlan:
        pass


class ExecutionEngine(ABC):
    @abstractmethod
    def execute(self, plan: ExecutionPlan) -> ExecutionResult:
        pass

    @abstractmethod
    def get_state(self, execution_id: str) -> ExecutionState:
        pass


class LLMProvider(ABC):
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        pass


class EmbeddingProvider(ABC):
    @abstractmethod
    def get_embedding(self, text: str) -> list[float]:
        pass


class PlatformClient(ABC):
    @abstractmethod
    def execute_operation(
        self, operation: str, parameters: dict[str, Any]
    ) -> dict[str, Any]:  # noqa: E501
        pass


class ExecutionReporter(ABC):
    @abstractmethod
    def generate_report(self, result: ExecutionResult) -> ExecutionReport:
        pass
