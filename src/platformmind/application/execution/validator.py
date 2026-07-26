"""
Execution Validator.
"""

from typing import Any

from platformmind.domain.models.execution import ExecutionStep


class ExecutionValidator:
    """
    Validates step inputs and outputs against schemas.
    """

    def validate_inputs(self, step: ExecutionStep, tool_schema: type) -> Any:
        """
        Validates inputs against the tool's expected Pydantic schema.
        Raises ValueError if invalid.
        """
        try:
            return tool_schema(**step.inputs)
        except Exception as e:
            raise ValueError(f"Input validation failed for step {step.step_id}: {e}")

    def validate_outputs(self, step: ExecutionStep, output: Any) -> bool:
        """
        Ensures the tool output conforms to expected structures.
        """
        return True  # Real implementation would validate against an output schema
