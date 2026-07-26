"""
Embedding Provider Interface.
"""

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """
    Contract for any embedding generation provider.
    """

    @abstractmethod
    async def embed_text(self, text: str) -> list[float]:
        pass

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass
