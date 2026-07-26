"""
LLM Provider Interface.
"""

from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    """
    Contract for any LLM provider.
    """

    @abstractmethod
    async def generate_text(self, prompt: str) -> str:
        pass

    @abstractmethod
    async def structured_completion(
        self, prompt: str, schema: dict[str, Any]
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def chat(self, messages: list[dict[str, Any]]) -> str:
        pass

    @abstractmethod
    async def summarize(self, text: str) -> str:
        pass

    @abstractmethod
    async def classify(self, text: str, categories: list[str]) -> str:
        pass

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """Optional if embedding provider is separate, but common in LLMs."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass
