"""
Learning Reports.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class LearningReport:
    """
    Structured learning report demonstrating measurable improvements.
    """

    execution_id: str
    current_metrics: dict[str, Any]
    historical_averages: dict[str, Any]
    improvements: dict[str, float]
    trends: list[str]
    recommendations: list[str]
