"""
Memory Engine Interface.
"""

from abc import ABC, abstractmethod
from typing import Any


class MemoryEngine(ABC):
    """
    Contract for semantic memory operations.
    """

    @abstractmethod
    async def store_execution(self, execution_data: dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def retrieve_similar(
        self, query: str, limit: int = 5
    ) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def store_capability(self, capability_data: dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def retrieve_capability(self, query: str) -> dict[str, Any]:
        pass

    @abstractmethod
    async def store_constraint(self, constraint_data: dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def retrieve_constraints(self, context: str) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def compact_memory(self) -> bool:
        pass

    @abstractmethod
    async def rank_memories(
        self, memories: list[dict[str, Any]], context: str
    ) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def summarize(self, memories: list[dict[str, Any]]) -> str:
        pass
