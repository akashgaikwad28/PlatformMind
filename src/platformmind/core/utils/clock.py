"""
Clock utility.
"""

from datetime import datetime, timezone


class Clock:
    """
    Utility for time operations.
    """

    @staticmethod
    def now() -> datetime:
        """
        Get current UTC time.
        """
        return datetime.now(timezone.utc)
