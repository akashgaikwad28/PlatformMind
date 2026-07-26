"""
Learning Metric Domain Model.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from platformmind.core.utils.clock import Clock


class LearningMetric(BaseModel):
    """
    Represents historical execution metrics for learning.
    """

    id: str
    capability_id: str
    successes: int = 0
    failures: int = 0
    total_execution_time: float = 0.0
    updated_at: datetime = Field(default_factory=Clock.now)

    model_config = ConfigDict(frozen=True)
