"""
Logging configuration for PlatformMind.
"""

import sys
from typing import Any

from loguru import logger

from platformmind.core.config.settings import settings


def setup_logger() -> None:
    """
    Configure Loguru logger with console and file handlers.
    """
    logger.remove()

    # Console logging
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )

    # File logging
    logger.add(
        "logs/platformmind_{time:YYYY-MM-DD}.log",
        rotation="00:00",  # Daily rotation
        retention="30 days",
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",  # noqa: E501  # noqa: E501
        serialize=False,  # Set to True for JSON structured logging if desired
    )


def get_logger() -> Any:
    """
    Get the configured logger instance.
    """
    return logger
