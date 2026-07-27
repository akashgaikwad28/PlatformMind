import functools
from typing import Callable


def trace_step(span_name: str):
    """
    No-op decorator. OpenTelemetry is disabled to prevent conflicts with Langfuse
    and to stop localhost:4317 timeout errors in Render.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
