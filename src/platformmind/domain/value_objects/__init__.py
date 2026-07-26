"""
Immutable Value Objects for PlatformMind Domain.
"""

import uuid

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ExecutionId(BaseModel):
    value: str = Field(default_factory=lambda: str(uuid.uuid4()))

    model_config = ConfigDict(frozen=True)


class InstructionId(BaseModel):
    value: str = Field(default_factory=lambda: str(uuid.uuid4()))

    model_config = ConfigDict(frozen=True)


class CapabilityId(BaseModel):
    value: str = Field(default_factory=lambda: str(uuid.uuid4()))

    model_config = ConfigDict(frozen=True)


class MemoryId(BaseModel):
    value: str = Field(default_factory=lambda: str(uuid.uuid4()))

    model_config = ConfigDict(frozen=True)


class RepositoryName(BaseModel):
    owner: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)

    model_config = ConfigDict(frozen=True)

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.name}"


class IssueNumber(BaseModel):
    value: int = Field(..., gt=0)

    model_config = ConfigDict(frozen=True)


class BranchName(BaseModel):
    value: str = Field(..., min_length=1)

    model_config = ConfigDict(frozen=True)

    @model_validator(mode="after")
    def validate_branch_name(self) -> "BranchName":
        if " " in self.value:
            raise ValueError("Branch name cannot contain spaces")
        return self


class ExecutionDuration(BaseModel):
    seconds: float = Field(..., ge=0.0)

    model_config = ConfigDict(frozen=True)


class ConfidenceScore(BaseModel):
    value: float = Field(..., ge=0.0, le=1.0)

    model_config = ConfigDict(frozen=True)


class SimilarityScore(BaseModel):
    value: float = Field(..., ge=-1.0, le=1.0)

    model_config = ConfigDict(frozen=True)
