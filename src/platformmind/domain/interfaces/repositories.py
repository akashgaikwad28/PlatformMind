"""
Domain Repository Interfaces.
"""

from abc import ABC, abstractmethod

from platformmind.domain.models.capability import Capability
from platformmind.domain.models.constraint import Constraint
from platformmind.domain.models.memory import ExecutionRecord, MemoryEntry
from platformmind.domain.value_objects import CapabilityId, ExecutionId, MemoryId


class MemoryRepository(ABC):
    @abstractmethod
    def save(self, memory: MemoryEntry) -> None:
        pass

    @abstractmethod
    def get_by_id(self, memory_id: MemoryId) -> MemoryEntry | None:
        pass

    @abstractmethod
    def search_similar(self, query: str, limit: int = 5) -> list[MemoryEntry]:
        pass


class CapabilityRepository(ABC):
    @abstractmethod
    def save(self, capability: Capability) -> None:
        pass

    @abstractmethod
    def get_by_id(self, capability_id: CapabilityId) -> Capability | None:
        pass

    @abstractmethod
    def list_all(self) -> list[Capability]:
        pass


class ExecutionRepository(ABC):
    @abstractmethod
    def save(self, record: ExecutionRecord) -> None:
        pass

    @abstractmethod
    def get_by_id(self, execution_id: ExecutionId) -> ExecutionRecord | None:
        pass


class ConstraintRepository(ABC):
    @abstractmethod
    def save(self, constraint: Constraint) -> None:
        pass

    @abstractmethod
    def list_all(self) -> list[Constraint]:
        pass


class LearningRepository(ABC):
    @abstractmethod
    def update_metrics(
        self, capability_id: CapabilityId, success: bool, execution_time: float
    ) -> None:  # noqa: E501
        pass
