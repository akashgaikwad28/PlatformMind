import json
from typing import Any

from groq import AsyncGroq

from platformmind.application.interfaces.llm.llm_provider import LLMProvider
from platformmind.core.telemetry.llm_tracer import observe


class GroqProvider(LLMProvider):
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        import os
        self.model = model
        # Initialize Groq client using environment variable GROQ_API_KEY, fallback for tests
        api_key = os.environ.get("GROQ_API_KEY", "dummy_test_key")
        self.client = AsyncGroq(api_key=api_key)
        self.max_context_chars = 30000

    async def _execute_with_retry(self, action: Any, *args: Any, **kwargs: Any) -> Any:
        import asyncio

        from groq import APIConnectionError, RateLimitError

        max_retries = 3
        base_delay = 1.0

        for attempt in range(max_retries):
            try:
                return await action(*args, **kwargs)
            except (RateLimitError, APIConnectionError):
                if attempt == max_retries - 1:
                    raise
                delay = base_delay * (2**attempt)
                await asyncio.sleep(delay)
            except Exception:
                raise

    def _truncate(self, text: str) -> str:
        if len(text) > self.max_context_chars:
            return text[: self.max_context_chars] + "... [TRUNCATED]"
        return text

    @observe(as_type="generation")
    async def generate_text(self, prompt: str) -> str:
        prompt = self._truncate(prompt)

        async def _call():
            completion = await self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            )
            return completion.choices[0].message.content or ""

        return await self._execute_with_retry(_call)

    @observe(as_type="generation")
    async def structured_completion(
        self, prompt: str, schema: dict[str, Any]
    ) -> dict[str, Any]:
        prompt = self._truncate(prompt)

        async def _call():
            system_msg = (
                f"You must respond ONLY with valid JSON that matches this schema: {json.dumps(schema)}\n"
                "Do not wrap it in markdown block quotes. Just the raw JSON object."
            )
            completion = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt},
                ],
                model=self.model,
                response_format={"type": "json_object"},
            )
            return completion.choices[0].message.content or "{}"

        content = await self._execute_with_retry(_call)
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {}

    @observe(as_type="generation")
    async def chat(self, messages: list[dict[str, Any]]) -> str:
        # Truncate content in messages if necessary
        for m in messages:
            if "content" in m and isinstance(m["content"], str):
                m["content"] = self._truncate(m["content"])

        async def _call():
            completion = await self.client.chat.completions.create(
                messages=messages,  # type: ignore
                model=self.model,
            )
            return completion.choices[0].message.content or ""

        return await self._execute_with_retry(_call)

    async def summarize(self, text: str) -> str:
        return await self.generate_text(f"Summarize this:\n\n{text}")

    async def classify(self, text: str, categories: list[str]) -> str:
        prompt = f"Classify the following text into exactly ONE of these categories: {categories}\nText: {text}"
        res = await self.generate_text(prompt)
        # naive matching for demo
        for cat in categories:
            if cat.lower() in res.lower():
                return cat
        return categories[0] if categories else ""

    async def embed(self, text: str) -> list[float]:
        # Groq currently does not provide native embeddings in the same way OpenAI does,
        # Fallback to deterministic vector generation since the current API tier lacks a native embeddings endpoint.
        import hashlib

        h = hashlib.sha256(text.encode()).digest()
        # Create a basic pseudo-embedding (normalized)
        vec = [float(x) / 255.0 for x in h[:10]]
        return vec

    async def health_check(self) -> bool:
        try:
            await self.generate_text("test")
            return True
        except Exception:
            return False
