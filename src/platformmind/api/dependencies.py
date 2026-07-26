"""
API Dependencies.
"""

from typing import Any

from fastapi import Request

# Service resolution fallbacks for dependency injection
# In a real app, these would return instances of the Application Services


def get_reporting_engine(request: Request) -> Any:
    return request.app.state.reporting_engine


def get_metrics_engine(request: Request) -> Any:
    return (
        request.app.state.learning_engine
    )  # Or metrics engine depending on architecture


def get_execution_engine(request: Request) -> Any:
    return request.app.state.execution_engine


def get_memory_engine(request: Request) -> Any:
    return request.app.state.memory_engine


def get_capabilities_engine(request: Request) -> Any:
    return (
        request.app.state.execution_engine
    )  # PlatformMindAppService provides native + synthesized capabilities


def get_synthesis_engine(request: Request) -> Any:
    return getattr(request.app.state, "synthesis_engine", None)
