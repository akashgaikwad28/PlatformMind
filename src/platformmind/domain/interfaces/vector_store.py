from abc import ABC, abstractmethod
from typing import List


class VectorStore(ABC):
    @abstractmethod
    def add(self, id: str, embedding: List[float], metadata: dict[str, str]) -> None:
        pass
