"""
Rollback Manager.
"""

from typing import Awaitable, Callable

from platformmind.infrastructure.logging.logger import get_logger

logger = get_logger()


class RollbackManager:
    """
    Manages compensatory actions for steps that have already succeeded.
    """

    def __init__(self) -> None:
        self._compensations: list[Callable[[], Awaitable[None]]] = []

    def register_compensation(self, action: Callable[[], Awaitable[None]]) -> None:
        """Register a compensatory action to be executed during rollback."""
        self._compensations.append(action)

    async def rollback(self) -> bool:
        """
        Executes all registered compensations in reverse order.
        Returns True if all succeeded, False if any failed.
        """
        success = True
        for compensation in reversed(self._compensations):
            try:
                await compensation()
            except Exception as e:
                logger.error(f"Rollback compensation failed: {e}")
                success = False
        return success
