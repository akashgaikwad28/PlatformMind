"""
Tool Registry.
"""

from platformmind.infrastructure.github.tools.base_tool import BaseTool


class ToolRegistry:
    """
    Resolves tool names to actual Tool instances.
    """

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, name: str, tool: BaseTool) -> None:
        self._tools[name] = tool

    def get(self, name: str) -> BaseTool:
        if name not in self._tools:
            raise ValueError(f"Tool {name} not found in registry")
        return self._tools[name]
