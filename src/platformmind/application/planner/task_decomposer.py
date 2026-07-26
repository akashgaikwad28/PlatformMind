"""
Task Decomposer.
"""

import os
from typing import Any

from platformmind.application.interfaces.llm.llm_provider import LLMProvider


class TaskDecomposer:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider
        self.prompt_path = os.path.join(
            os.path.dirname(__file__), "prompts", "decomposition.txt"
        )

    async def decompose(
        self, instruction: str, previous_results: list[dict[str, Any]] = None
    ) -> list[dict[str, Any]]:
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()

        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "description": {"type": "string"},
                    "depends_on": {"type": "array", "items": {"type": "string"}},
                    "inputs": {"type": "object"},
                },
                "required": ["id", "description", "depends_on"],
            },
        }

        prompt = f"{system_prompt}\nInstruction: {instruction}"

        if previous_results:
            import json

            prompt += f"\n\nPrevious Execution Results:\n{json.dumps(previous_results, indent=2)}"

        # We can simulate parsing for LLM providers that don't natively support top-level arrays
        # by wrapping it in an object, but standard JSON schema allows array root.

        # Note: If the LLM wrapper needs object root, wrap it:
        obj_schema = {
            "type": "object",
            "properties": {"tasks": schema},
            "required": ["tasks"],
        }

        result = await self.llm_provider.structured_completion(prompt, obj_schema)
        return result.get("tasks", [])
