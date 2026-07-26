"""
GitHub Exceptions.
"""


class GitHubError(Exception):
    """Base exception for all GitHub-related errors."""

    pass


class GitHubUnauthorizedError(GitHubError):
    """Raised for 401 Unauthorized errors."""

    pass


class GitHubForbiddenError(GitHubError):
    """Raised for 403 Forbidden errors."""

    pass


class GitHubNotFoundError(GitHubError):
    """Raised for 404 Not Found errors."""

    pass


class GitHubConflictError(GitHubError):
    """Raised for 409 Conflict errors."""

    pass


class GitHubValidationError(GitHubError):
    """Raised for 422 Validation errors."""

    pass


class GitHubRateLimitError(GitHubError):
    """Raised for 429 Rate Limit Exceeded errors."""

    def __init__(self, message: str, reset_time: int = 0):
        super().__init__(message)
        self.reset_time = reset_time


class GitHubServerError(GitHubError):
    """Raised for 5xx Server errors."""

    pass


class GitHubConnectionError(GitHubError):
    """Raised for timeouts or connection failures."""

    pass
