"""
Generic Repository Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
ID = TypeVar("ID")


class BaseRepository(Generic[T, ID], ABC):
    """
    Base generic repository contract.
    """

    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: ID) -> T | None:
        pass

    @abstractmethod
    async def list(self) -> list[T]:
        pass

    @abstractmethod
    async def update(self, entity_id: ID, entity: T) -> T:
        pass

    @abstractmethod
    async def delete(self, entity_id: ID) -> bool:
        pass

    @abstractmethod
    async def exists(self, entity_id: ID) -> bool:
        pass


class ExecutionRepository(BaseRepository, ABC):
    """Repository for Execution data."""

    pass


class CapabilityRepository(BaseRepository, ABC):
    """Repository for Capability data."""

    pass


class ConstraintRepository(BaseRepository, ABC):
    """Repository for Constraint data."""

    pass


class MemoryRepository(BaseRepository, ABC):
    """Repository for Memory data."""

    pass


class LearningRepository(BaseRepository, ABC):
    """Repository for Learning metrics and data."""

    pass


class ReportRepository(BaseRepository, ABC):
    """Repository for Report data."""

    pass
