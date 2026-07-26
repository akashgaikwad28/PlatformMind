"""
Constraint Domain Model.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from platformmind.core.utils.clock import Clock
from platformmind.domain.enums import ConstraintSeverity, ConstraintType


class Constraint(BaseModel):
    """
    Represents learned platform constraints.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: ConstraintType
    description: str
    severity: ConstraintSeverity
    discovered_at: datetime = Field(default_factory=Clock.now)

    model_config = ConfigDict(frozen=True)
