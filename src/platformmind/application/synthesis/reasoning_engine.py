"""
Reasoning Engine.
"""

from typing import Any

from platformmind.application.interfaces.llm.llm_provider import LLMProvider
from platformmind.application.synthesis.gap_detector import CapabilityGap


class ReasoningEngine:
    """
    Reasons about how to fulfill a missing capability.
    """

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def reason(self, gap: CapabilityGap) -> dict[str, Any]:
        """
        Uses LLM to deduce required tools and strategies.
        """
        prompt = f"""
        You are an autonomous agent capable of synthesizing new capabilities.
        The planner failed to execute the following instruction because it lacks a native tool.
        
        Instruction: {gap.instruction}
        Missing Workflow: {gap.missing_workflow}
        Missing Tools: {gap.missing_tools}
        
        Analyze if this task can be synthesized using a combination of generic HTTP calls or by composing existing basic tools like search_issues, create_issue, assign_label, update_issue, close_issue, create_comment.
        """

        schema = {
            "type": "object",
            "properties": {
                "is_synthesizable": {
                    "type": "boolean",
                    "description": "Whether this gap can be filled dynamically",
                },
                "suggested_tools": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of native tools to compose",
                },
                "strategy": {
                    "type": "string",
                    "description": "Step-by-step strategy to synthesize",
                },
            },
            "required": ["is_synthesizable", "suggested_tools", "strategy"],
        }

        result = await self.llm.structured_completion(prompt, schema)
        return result
