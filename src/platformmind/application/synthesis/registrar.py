"""
Capability Registrar.
"""

from typing import Any

from platformmind.domain.models.execution import ExecutionPlan


class CapabilityRegistrar:
    """
    Persists successful capabilities to Memory.
    """

    def register(self, design: dict[str, Any], plan: ExecutionPlan) -> str:
        """
        Registers the capability and returns its ID.
        """
        capability_id = f"cap_{design['name']}"
        # In reality, this saves to CapabilityMemory
        return capability_id
