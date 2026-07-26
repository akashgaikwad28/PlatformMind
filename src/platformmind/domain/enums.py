"""
Domain Enums for PlatformMind.
"""

from enum import Enum


class ExecutionStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    CANCELLED = "CANCELLED"


class CapabilityStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"


class InstructionPriority(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ConstraintSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ConstraintType(str, Enum):
    RATE_LIMIT = "RATE_LIMIT"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_UNAVAILABLE = "RESOURCE_UNAVAILABLE"
    BUSINESS_RULE = "BUSINESS_RULE"


class MemoryCategory(str, Enum):
    EXECUTION = "EXECUTION"
    CAPABILITY = "CAPABILITY"
    CONSTRAINT = "CONSTRAINT"
    LEARNING = "LEARNING"


class ToolType(str, Enum):
    GITHUB = "GITHUB"
    SYSTEM = "SYSTEM"
    DATA_PROCESSING = "DATA_PROCESSING"


class ExecutionStepStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class LearningStatus(str, Enum):
    NEW = "NEW"
    EVALUATING = "EVALUATING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"


class ConfidenceLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
