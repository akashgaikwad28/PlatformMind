"""
Capability Designer.
"""

from typing import Any


class CapabilityDesigner:
    """
    Designs the interface and metadata for the new capability.
    """

    def design(self, instruction: str, reasoning: dict[str, Any]) -> dict[str, Any]:
        return {
            "name": f"synthesized_capability_{hash(instruction) % 1000}",
            "description": f"Generated to fulfill: {instruction}",
            "required_tools": reasoning.get("suggested_tools", []),
            "version": "1.0.0",
        }
