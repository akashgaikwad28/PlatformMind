"""
Langfuse wrapper for LLM observability.

IMPORTANT: This module uses a lazy initialization pattern.
The @observe decorator is applied at class-definition time, but the actual
Langfuse client is initialized lazily on first use. This avoids the common
pitfall of importing Langfuse before environment variables are loaded.

Compatible with Langfuse SDK v2 (langfuse.decorators.observe) and
v3/v4 (langfuse.observe at top level).
"""

import functools
import logging
import os
import threading
from typing import Any, Callable

logger = logging.getLogger(__name__)

_observe_lock = threading.Lock()


def _get_langfuse_observe():
    """
    Import the correct @observe decorator depending on SDK version.

    - v3/v4: `from langfuse import observe`
    - v2: `from langfuse.decorators import observe`
    """
    # Try v3/v4 first (top-level import)
    try:
        from langfuse import observe as langfuse_observe
        return langfuse_observe
    except ImportError:
        pass

    # Fall back to v2
    from langfuse.decorators import observe as langfuse_observe
    return langfuse_observe


def observe(*args, **kwargs):
    """
    Lazy wrapper for Langfuse @observe.

    Instead of calling langfuse_observe() at decoration time (which would
    initialize the Langfuse SDK before env vars are loaded), this returns
    a decorator that defers to Langfuse at CALL time.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*a: Any, **k: Any) -> Any:
            # Attempt to use Langfuse at call time (env vars are loaded by now)
            try:
                public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
                secret_key = os.environ.get("LANGFUSE_SECRET_KEY")

                if not public_key or not secret_key:
                    return await func(*a, **k)

                # Thread-safe creation of the decorated function on first call
                if not hasattr(async_wrapper, "_langfuse_fn"):
                    with _observe_lock:
                        if not hasattr(async_wrapper, "_langfuse_fn"):
                            langfuse_observe = _get_langfuse_observe()
                            decorated = langfuse_observe(*args, **kwargs)(func)
                            async_wrapper._langfuse_fn = decorated  # type: ignore

                return await async_wrapper._langfuse_fn(*a, **k)  # type: ignore
            except ImportError:
                return await func(*a, **k)
            except Exception as e:
                logger.warning(f"Langfuse observe failed, falling back to raw call: {e}")
                return await func(*a, **k)

        @functools.wraps(func)
        def sync_wrapper(*a: Any, **k: Any) -> Any:
            try:
                public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
                secret_key = os.environ.get("LANGFUSE_SECRET_KEY")

                if not public_key or not secret_key:
                    return func(*a, **k)

                # Thread-safe creation of the decorated function on first call
                if not hasattr(sync_wrapper, "_langfuse_fn"):
                    with _observe_lock:
                        if not hasattr(sync_wrapper, "_langfuse_fn"):
                            langfuse_observe = _get_langfuse_observe()
                            decorated = langfuse_observe(*args, **kwargs)(func)
                            sync_wrapper._langfuse_fn = decorated  # type: ignore

                return sync_wrapper._langfuse_fn(*a, **k)  # type: ignore
            except ImportError:
                return func(*a, **k)
            except Exception as e:
                logger.warning(f"Langfuse observe failed, falling back to raw call: {e}")
                return func(*a, **k)

        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
