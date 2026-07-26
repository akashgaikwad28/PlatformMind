"""
Memory Summarizer Component.
"""

from platformmind.application.interfaces.llm.llm_provider import LLMProvider


class MemorySummarizer:
    """
    Leverages LLM Provider to summarize execution strategies and extract broad lessons.
    """

    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def summarize_memories(self, context_data: str) -> str:
        prompt = f"Summarize the following execution memories to extract key successful strategies:\n{context_data}"
        return await self.llm_provider.summarize(prompt)
