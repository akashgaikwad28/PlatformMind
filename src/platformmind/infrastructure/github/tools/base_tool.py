"""
Base Tool Implementation.
"""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

from platformmind.core.utils.clock import Clock
from platformmind.infrastructure.github.schemas.schemas import ToolResult

TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput")


class BaseTool(Generic[TInput]):
    """
    Abstract base class for GitHub tools.
    Provides validation, execution timing, and standard result wrapping.
    """

    name: str = "base_tool"
    description: str = "Base tool description"
    input_schema: type[TInput]

    async def run(self, **kwargs: Any) -> ToolResult:
        start_time = Clock.now()
        api_calls = 0
        status_code = None
        data = None
        warnings = []
        errors = []
        success = False

        try:
            # 1. Validate Input
            validated_input = self.input_schema(**kwargs)

            # 2. Execute (with a generic context hook to track API calls if needed)
            # The tool subclass defines `_execute`
            # _execute should return a tuple (data, status_code, api_calls)
            data, status_code, api_calls = await self._execute(validated_input)
            success = True

        except Exception as e:
            errors.append(str(e))
            success = False

        execution_time = (Clock.now() - start_time).total_seconds()

        return ToolResult(
            success=success,
            tool_name=self.name,
            execution_time=execution_time,
            api_calls=api_calls,
            status_code=status_code,
            data=data,
            warnings=warnings,
            errors=errors,
        )

    async def _execute(self, inputs: TInput) -> tuple[Any, int | None, int]:
        """
        To be implemented by specific tools.
        Returns (result_data, http_status_code, number_of_api_calls).
        """
        raise NotImplementedError()
