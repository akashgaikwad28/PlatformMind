from abc import ABC, abstractmethod
from typing import List

from platformmind.domain.capabilities.capability import Capability


class CapabilityRepository(ABC):
    @abstractmethod
    def save(self, capability: Capability) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Capability]:
        pass
