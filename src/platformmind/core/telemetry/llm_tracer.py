"""
Langfuse wrapper for LLM observability.
"""

import functools
import logging
import os
from typing import Callable

try:
    from langfuse.decorators import observe as langfuse_observe

    HAS_LANGFUSE = True
except ImportError:
    HAS_LANGFUSE = False

logger = logging.getLogger(__name__)


def observe(*args, **kwargs):
    """
    Wrapper for Langfuse observe.
    Gracefully degrades to a no-op if Langfuse keys are missing or the package is not installed.
    """

    def noop_decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*a, **k):
            return func(*a, **k)

        @functools.wraps(func)
        async def async_wrapper(*a, **k):
            return await func(*a, **k)

        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return wrapper

    if not HAS_LANGFUSE:
        logger.error("HAS_LANGFUSE is False. Langfuse library is not installed correctly.")
        return noop_decorator

    # Check for keys. If missing, Langfuse will warn, but we can suppress or just return no-op.
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    if not public_key or not secret_key:
        logger.error(f"Langfuse keys missing (pub={bool(public_key)}, sec={bool(secret_key)}). LLM Tracing disabled.")
        return noop_decorator

    return langfuse_observe(*args, **kwargs)
