"""
Domain exceptions for PlatformMind.
"""


class PlatformMindException(Exception):
    """
    Base exception for all PlatformMind errors.
    """

    pass


class ConfigurationException(PlatformMindException):
    """
    Raised when there is a configuration error.
    """

    pass


class ValidationException(PlatformMindException):
    """
    Raised when validation fails.
    """

    pass


class PlanningException(PlatformMindException):
    """
    Raised when planning fails.
    """

    pass


class ExecutionException(PlatformMindException):
    """
    Raised when execution of a plan fails.
    """

    pass


class MemoryException(PlatformMindException):
    """
    Raised when a memory operation fails.
    """

    pass


class CapabilityException(PlatformMindException):
    """
    Raised when capability synthesis or retrieval fails.
    """

    pass


class LearningException(PlatformMindException):
    """
    Raised when the learning engine encounters an error.
    """

    pass


class InfrastructureException(PlatformMindException):
    """
    Raised when an infrastructure component fails.
    """

    pass


class GitHubException(InfrastructureException):
    """
    Raised when a GitHub API operation fails.
    """

    pass


class LLMException(InfrastructureException):
    """
    Raised when an LLM provider operation fails.
    """

    pass


class RepositoryException(InfrastructureException):
    """
    Raised when a database repository operation fails.
    """

    pass


class InvalidInstructionException(PlatformMindException):
    """
    Raised when an instruction is invalid.
    """

    pass


class InvalidExecutionPlanException(PlatformMindException):
    """
    Raised when an execution plan is invalid.
    """

    pass


class InvalidCapabilityException(PlatformMindException):
    """
    Raised when a capability is invalid.
    """

    pass


class DependencyCycleException(PlatformMindException):
    """
    Raised when a dependency cycle is detected in an execution plan.
    """

    pass


class ConstraintViolationException(PlatformMindException):
    """
    Raised when an action violates a known platform constraint.
    """

    pass
