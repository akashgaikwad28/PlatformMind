"""
Execution Analyzer.
"""

from typing import Any

from platformmind.domain.models.execution import ExecutionResult


class ExecutionAnalyzer:
    """
    Extracts raw facts from an ExecutionResult.
    """

    def analyze(self, result: ExecutionResult) -> dict[str, Any]:
        return {
            "execution_id": result.execution_id.value,
            "status": result.status.value,
            "api_calls": result.api_calls,
            "retries": result.retries,
            "execution_time": result.execution_time.seconds,
            "errors": result.errors,
            "warnings": result.warnings,
        }
