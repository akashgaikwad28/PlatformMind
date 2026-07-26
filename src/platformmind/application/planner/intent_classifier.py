"""
Intent Classifier.
"""

import os

from platformmind.application.interfaces.llm.llm_provider import LLMProvider


class IntentClassifier:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider
        self.prompt_path = os.path.join(
            os.path.dirname(__file__), "prompts", "intents.txt"
        )

    async def classify(self, normalized_instruction: str) -> tuple[str, float]:
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()

        schema = {
            "type": "object",
            "properties": {
                "intent": {"type": "string"},
                "confidence": {"type": "number"},
            },
            "required": ["intent", "confidence"],
        }

        prompt = f"{system_prompt}\nInstruction: {normalized_instruction}"
        result = await self.llm_provider.structured_completion(prompt, schema)

        intent = result.get("intent", "COMPOUND_WORKFLOW").upper()
        confidence = float(result.get("confidence", 0.5))

        return intent, confidence
