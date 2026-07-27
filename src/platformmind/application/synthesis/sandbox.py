"""
Sandbox Tester.
"""

from platformmind.application.interfaces.llm.llm_provider import LLMProvider
from platformmind.domain.models.execution import ExecutionPlan


class SandboxTester:
    """
    Simulates execution to verify the generated capability using LLM static analysis.
    """

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def test(self, plan: ExecutionPlan) -> bool:
        """
        Uses LLM to perform a dry-run static analysis of the generated execution plan.
        """
        prompt = f"""
        You are a sandbox testing environment.
        Please evaluate the following execution plan for a newly synthesized capability.
        Determine if the sequence of API calls is logical, safe, and likely to succeed.
        
        Plan Steps: {[step.tool_name for step in plan.steps] if isinstance(plan, ExecutionPlan) and hasattr(plan, 'steps') else str(plan)}
        """
        
        schema = {
            "type": "object",
            "properties": {
                "is_safe": {"type": "boolean"},
                "reasoning": {"type": "string"}
            },
            "required": ["is_safe", "reasoning"]
        }
        
        try:
            result = await self.llm.structured_completion(prompt, schema)
            return result.get("is_safe", False)
        except Exception:
            return False
