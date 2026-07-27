"""
Singleton Langfuse client for PlatformMind.

Provides a single shared Langfuse instance to avoid creating a new client
(with a new HTTP connection, auth handshake, and batch queue) on every request.

Compatible with Langfuse SDK v3/v4 which uses get_client() instead of Langfuse().
Falls back to legacy Langfuse() for older SDK versions (v2.x).
"""

import logging
import os
import threading
from typing import Optional

logger = logging.getLogger(__name__)

_langfuse_client = None
_lock = threading.Lock()
_sdk_version: Optional[int] = None  # 2, 3, or 4


def _detect_sdk_version() -> int:
    """Detect the installed Langfuse SDK major version."""
    try:
        import importlib.metadata
        version_str = importlib.metadata.version("langfuse")
        major = int(version_str.split(".")[0])
        return major
    except Exception:
        # If we can't detect, try the new API first
        try:
            from langfuse import get_client  # noqa: F401
            return 3  # v3+ has get_client
        except ImportError:
            return 2  # v2 uses Langfuse()


def get_langfuse():
    """
    Return the shared Langfuse client, creating it on first call.

    Uses get_client() for SDK v3+ and Langfuse() for SDK v2.
    Returns None if API keys are not configured, allowing callers
    to gracefully skip tracing.
    """
    global _langfuse_client, _sdk_version

    if _langfuse_client is not None:
        return _langfuse_client

    with _lock:
        # Double-checked locking
        if _langfuse_client is not None:
            return _langfuse_client

        public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
        secret_key = os.environ.get("LANGFUSE_SECRET_KEY")

        if not public_key or not secret_key:
            logger.info("Langfuse keys not configured — tracing disabled")
            return None

        try:
            _sdk_version = _detect_sdk_version()
            logger.info(f"Detected Langfuse SDK major version: {_sdk_version}")

            if _sdk_version >= 3:
                from langfuse import get_client
                _langfuse_client = get_client()
            else:
                from langfuse import Langfuse
                _langfuse_client = Langfuse()

            logger.info("Langfuse client initialized successfully")
            return _langfuse_client
        except ImportError:
            logger.warning("langfuse package not installed — tracing disabled")
            return None
        except Exception as e:
            logger.error(f"Failed to initialize Langfuse client: {e}")
            return None


def get_sdk_version() -> int:
    """Return the detected SDK major version (2, 3, or 4)."""
    global _sdk_version
    if _sdk_version is None:
        _sdk_version = _detect_sdk_version()
    return _sdk_version


def shutdown_langfuse() -> None:
    """
    Flush pending events and shut down the Langfuse client gracefully.

    Call this during application shutdown to ensure the last batch of
    traces is not lost.
    """
    global _langfuse_client

    if _langfuse_client is None:
        return

    try:
        if hasattr(_langfuse_client, "shutdown"):
            _langfuse_client.shutdown()
        elif hasattr(_langfuse_client, "flush"):
            _langfuse_client.flush()
        logger.info("Langfuse client shut down successfully")
    except Exception as e:
        logger.warning(f"Error shutting down Langfuse client: {e}")
    finally:
        _langfuse_client = None
