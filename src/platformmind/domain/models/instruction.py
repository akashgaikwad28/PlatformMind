"""
Instruction Domain Model.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from platformmind.core.utils.clock import Clock
from platformmind.domain.enums import ConfidenceLevel, InstructionPriority
from platformmind.domain.value_objects import InstructionId


class Instruction(BaseModel):
    """
    Represents a natural language instruction.
    """

    id: InstructionId = Field(default_factory=InstructionId)
    original_text: str = Field(..., min_length=1)
    normalized_text: str = Field(default="")
    created_at: datetime = Field(default_factory=Clock.now)
    metadata: dict[str, Any] = Field(default_factory=dict)
    priority: InstructionPriority = Field(default=InstructionPriority.NORMAL)
    confidence: ConfidenceLevel = Field(default=ConfidenceLevel.LOW)

    model_config = ConfigDict(frozen=True)

    @model_validator(mode="before")
    @classmethod
    def set_normalized_text(cls, data: Any) -> Any:
        if isinstance(data, dict):
            orig = data.get("original_text")
            if not data.get("normalized_text") and isinstance(orig, str):
                data["normalized_text"] = orig.strip().lower()
        return data
