"""
Vector Store Interface.
"""

from abc import ABC, abstractmethod
from typing import Any


class VectorStore(ABC):
    """
    Contract for vector database interactions (e.g., ChromaDB, Qdrant).
    """

    @abstractmethod
    async def index(
        self, vector_id: str, vector: list[float], payload: dict[str, Any]
    ) -> bool:
        pass

    @abstractmethod
    async def search(
        self, query_vector: list[float], limit: int = 5
    ) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def delete(self, vector_id: str) -> bool:
        pass

    @abstractmethod
    async def update(
        self, vector_id: str, vector: list[float], payload: dict[str, Any]
    ) -> bool:
        pass

    @abstractmethod
    async def similarity_search(
        self, query_vector: list[float], limit: int = 5
    ) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass
