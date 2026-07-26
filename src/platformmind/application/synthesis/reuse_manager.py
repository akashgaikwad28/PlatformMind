"""
Reuse Manager.
"""

from typing import Any


class ReuseManager:
    """
    Provides search capabilities to the Planner to find existing capabilities.
    """

    def __init__(self):
        self._cache = {}  # Simulated memory

    def find_capability(self, instruction: str) -> dict[str, Any] | None:
        """
        Searches memory for a matching capability.
        """
        # Simulated lookup
        for cap in self._cache.values():
            if instruction.lower() in cap.get("description", "").lower():
                return cap
        return None

    def add_to_cache(self, cap_id: str, design: dict[str, Any]) -> None:
        self._cache[cap_id] = design
