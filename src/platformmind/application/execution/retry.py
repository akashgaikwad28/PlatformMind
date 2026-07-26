"""
Retry Manager.
"""

import asyncio
from typing import Any, Awaitable, Callable


class RetryManager:
    """
    Manages exponential backoff for transient failures.
    """

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    async def execute_with_retry(
        self,
        action: Callable[[], Awaitable[Any]],
        is_retryable: Callable[[Exception], bool],
    ) -> Any:
        attempts = 0
        while True:
            try:
                return await action()
            except Exception as e:
                attempts += 1
                if attempts > self.max_retries or not is_retryable(e):
                    raise

                delay = self.base_delay * (2 ** (attempts - 1))
                await asyncio.sleep(delay)
