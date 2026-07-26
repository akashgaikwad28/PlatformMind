"""
Capability Domain Model.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from platformmind.core.utils.clock import Clock
from platformmind.domain.enums import CapabilityStatus
from platformmind.domain.value_objects import CapabilityId


class Capability(BaseModel):
    """
    Represents reusable system capabilities.
    """

    id: CapabilityId = Field(default_factory=CapabilityId)
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    input_schema: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] = Field(default_factory=dict)
    execution_strategy: dict[str, Any] = Field(default_factory=dict)
    success_rate: float = Field(default=1.0)
    average_execution_time: float = Field(default=0.0)
    version: str = Field(default="1.0.0")
    created_at: datetime = Field(default_factory=Clock.now)
    status: CapabilityStatus = Field(default=CapabilityStatus.ACTIVE)

    model_config = ConfigDict(frozen=True)
