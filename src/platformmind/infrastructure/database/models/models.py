"""
SQLAlchemy ORM Models.
"""

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from platformmind.core.utils.clock import Clock
from platformmind.infrastructure.database.base import Base


class ExecutionRecordModel(Base):
    __tablename__ = "execution_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    instruction: Mapped[str] = mapped_column(String, nullable=False)
    execution_summary: Mapped[str] = mapped_column(String, nullable=False)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=Clock.now)


class CapabilityModel(Base):
    __tablename__ = "capabilities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    input_schema: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    output_schema: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    execution_strategy: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    success_rate: Mapped[float] = mapped_column(Float, default=1.0)
    average_execution_time: Mapped[float] = mapped_column(Float, default=0.0)
    version: Mapped[str] = mapped_column(String, default="1.0.0")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=Clock.now)
    status: Mapped[str] = mapped_column(String, default="ACTIVE")


class ConstraintModel(Base):
    __tablename__ = "constraints"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    discovered_at: Mapped[datetime] = mapped_column(DateTime, default=Clock.now)


class ReportModel(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    execution_id: Mapped[str] = mapped_column(String(36), nullable=False)
    content: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=Clock.now)


class LearningMetricModel(Base):
    __tablename__ = "learning_metrics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    capability_id: Mapped[str] = mapped_column(String(36), nullable=False)
    successes: Mapped[int] = mapped_column(Integer, default=0)
    failures: Mapped[int] = mapped_column(Integer, default=0)
    total_execution_time: Mapped[float] = mapped_column(Float, default=0.0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=Clock.now)
