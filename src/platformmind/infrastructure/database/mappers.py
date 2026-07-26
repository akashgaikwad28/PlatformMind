"""
Data Mappers (Domain <-> ORM).
"""

from platformmind.domain.enums import (
    CapabilityStatus,
    ConstraintSeverity,
    ConstraintType,
)
from platformmind.domain.models.capability import Capability
from platformmind.domain.models.constraint import Constraint
from platformmind.domain.models.learning import LearningMetric
from platformmind.domain.models.memory import ExecutionRecord
from platformmind.domain.value_objects import CapabilityId, ExecutionId
from platformmind.infrastructure.database.models.models import (
    CapabilityModel,
    ConstraintModel,
    ExecutionRecordModel,
    LearningMetricModel,
)


class ExecutionRecordMapper:
    @staticmethod
    def to_domain(model: ExecutionRecordModel) -> ExecutionRecord:
        return ExecutionRecord(
            execution_id=ExecutionId(value=model.id),
            instruction=model.instruction,
            execution_summary=model.execution_summary,
            metrics=model.metrics,
            timestamp=model.timestamp,
        )

    @staticmethod
    def to_orm(domain: ExecutionRecord) -> ExecutionRecordModel:
        return ExecutionRecordModel(
            id=domain.execution_id.value,
            instruction=domain.instruction,
            execution_summary=domain.execution_summary,
            metrics=domain.metrics,
            timestamp=domain.timestamp,
        )


class CapabilityMapper:
    @staticmethod
    def to_domain(model: CapabilityModel) -> Capability:
        return Capability(
            id=CapabilityId(value=model.id),
            name=model.name,
            description=model.description,
            input_schema=model.input_schema,
            output_schema=model.output_schema,
            execution_strategy=model.execution_strategy,
            success_rate=model.success_rate,
            average_execution_time=model.average_execution_time,
            version=model.version,
            created_at=model.created_at,
            status=CapabilityStatus(model.status),
        )

    @staticmethod
    def to_orm(domain: Capability) -> CapabilityModel:
        return CapabilityModel(
            id=domain.id.value,
            name=domain.name,
            description=domain.description,
            input_schema=domain.input_schema,
            output_schema=domain.output_schema,
            execution_strategy=domain.execution_strategy,
            success_rate=domain.success_rate,
            average_execution_time=domain.average_execution_time,
            version=domain.version,
            created_at=domain.created_at,
            status=domain.status.value,
        )


class ConstraintMapper:
    @staticmethod
    def to_domain(model: ConstraintModel) -> Constraint:
        return Constraint(
            id=model.id,
            type=ConstraintType(model.type),
            description=model.description,
            severity=ConstraintSeverity(model.severity),
            discovered_at=model.discovered_at,
        )

    @staticmethod
    def to_orm(domain: Constraint) -> ConstraintModel:
        return ConstraintModel(
            id=domain.id,
            type=domain.type.value,
            description=domain.description,
            severity=domain.severity.value,
            discovered_at=domain.discovered_at,
        )


class LearningMetricMapper:
    @staticmethod
    def to_domain(model: LearningMetricModel) -> LearningMetric:
        return LearningMetric(
            id=model.id,
            capability_id=model.capability_id,
            successes=model.successes,
            failures=model.failures,
            total_execution_time=model.total_execution_time,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_orm(domain: LearningMetric) -> LearningMetricModel:
        return LearningMetricModel(
            id=domain.id,
            capability_id=domain.capability_id,
            successes=domain.successes,
            failures=domain.failures,
            total_execution_time=domain.total_execution_time,
            updated_at=domain.updated_at,
        )
