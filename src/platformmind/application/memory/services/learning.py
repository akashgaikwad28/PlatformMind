"""
Learning Memory Service.
"""

from typing import Any

from platformmind.application.interfaces.repositories.repositories import (
    LearningRepository,
)


class LearningMemoryService:
    """
    Service for tracking planning/execution metrics and tool effectiveness.
    """

    def __init__(self, repository: LearningRepository):
        self.repository = repository

    async def get_historical_metrics(self) -> dict[str, Any]:
        records = await self.repository.list()

        # Calculate aggregates
        if not records:
            return {
                "total_time": 0.0,
                "total_calls": 0,
                "total_retries": 0,
            }

        total_time = sum(r.total_execution_time for r in records)
        return {
            "total_time": total_time / len(records) if records else 0.0,
            "total_calls": 5,  # Mocking calls and retries for now as domain model focused on time
            "total_retries": 1,
        }

    async def save_metrics(self, data: dict[str, Any]) -> None:
        import uuid

        from platformmind.domain.models.learning import LearningMetric

        # We save the metrics to the repository
        metric = LearningMetric(
            id=f"lm_{uuid.uuid4().hex[:8]}",
            capability_id=data.get("capability_id", "global"),
            successes=1 if data.get("status") == "SUCCESS" else 0,
            failures=1 if data.get("status") != "SUCCESS" else 0,
            total_execution_time=data.get("total_time", 0.0),
        )
        await self.repository.create(metric)
