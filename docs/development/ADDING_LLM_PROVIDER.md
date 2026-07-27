---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/application/interfaces/llm/llm_provider.py`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Adding an LLM Provider

## Purpose
Guide to swapping Groq for another provider like OpenAI or Anthropic.

## Internal Workflow

### 1. Implement the Interface
Create a new file in `src/platformmind/infrastructure/llm/openai_provider.py`.

```python
from platformmind.application.interfaces.llm.llm_provider import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        
    async def generate(self, prompt: str, system: str = None) -> str:
        # Map parameters to OpenAI API
        pass
        
    async def generate_structured(self, prompt: str, schema: BaseModel, system: str = None) -> BaseModel:
        # Map parameters to OpenAI Structured Outputs API
        pass
```

### 2. Update the Container
Open `src/platformmind/api/container.py`. Swap the instantiation:

```python
# llm_provider = GroqProvider(api_key=settings.GROQ_API_KEY)
llm_provider = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
```

## Important Considerations
- Different LLMs have different dialects for structured JSON output. Ensure the implementation strictly maps to Pydantic schemas.
- Update `ENVIRONMENT_VARIABLES.md` to reflect the new API key requirements.
