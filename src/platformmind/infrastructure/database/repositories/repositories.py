"""
Concrete Repository Implementations.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from platformmind.application.interfaces.repositories.repositories import (
    CapabilityRepository,
    ConstraintRepository,
    ExecutionRepository,
    LearningRepository,
)
from platformmind.domain.models.capability import Capability
from platformmind.domain.models.constraint import Constraint
from platformmind.domain.models.learning import LearningMetric
from platformmind.domain.models.memory import ExecutionRecord
from platformmind.domain.value_objects import CapabilityId, ExecutionId
from platformmind.infrastructure.database.mappers import (
    CapabilityMapper,
    ConstraintMapper,
    ExecutionRecordMapper,
    LearningMetricMapper,
)
from platformmind.infrastructure.database.models.models import (
    CapabilityModel,
    ConstraintModel,
    ExecutionRecordModel,
    LearningMetricModel,
)
from platformmind.infrastructure.database.repositories.base_repository import (
    BaseRepositoryImpl,
)


class ExecutionRepositoryImpl(
    BaseRepositoryImpl[ExecutionRecord, ExecutionRecordModel, ExecutionId],
    ExecutionRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ExecutionRecordModel, ExecutionRecordMapper)


class CapabilityRepositoryImpl(
    BaseRepositoryImpl[Capability, CapabilityModel, CapabilityId], CapabilityRepository
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, CapabilityModel, CapabilityMapper)

    # We can add list_all from the domain interface explicitly if needed
    async def list_all(self) -> list[Capability]:
        return await self.list()


class ConstraintRepositoryImpl(
    BaseRepositoryImpl[Constraint, ConstraintModel, str], ConstraintRepository
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ConstraintModel, ConstraintMapper)

    async def list_all(self) -> list[Constraint]:
        return await self.list()


class LearningRepositoryImpl(
    BaseRepositoryImpl[LearningMetric, LearningMetricModel, str], LearningRepository
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, LearningMetricModel, LearningMetricMapper)
