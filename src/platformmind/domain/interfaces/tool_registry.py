from abc import ABC, abstractmethod


class ToolRegistry(ABC):
    @abstractmethod
    def register_tool(self, name: str, tool: object) -> None:
        pass
