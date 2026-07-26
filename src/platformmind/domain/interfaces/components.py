"""
Component Domain Interfaces.
"""

from abc import ABC, abstractmethod

from platformmind.domain.models.capability import Capability
from platformmind.domain.models.execution import ExecutionResult
from platformmind.domain.models.instruction import Instruction
from platformmind.domain.models.memory import MemoryEntry


class CapabilitySynthesizer(ABC):
    @abstractmethod
    def synthesize(self, instruction: Instruction) -> Capability:
        pass


class MemoryRanker(ABC):
    @abstractmethod
    def rank(self, memories: list[MemoryEntry], context: str) -> list[MemoryEntry]:
        pass


class KnowledgeExtractor(ABC):
    @abstractmethod
    def extract(self, result: ExecutionResult) -> list[MemoryEntry]:
        pass


class ValidationService(ABC):
    @abstractmethod
    def validate(self, target: object) -> bool:
        pass
