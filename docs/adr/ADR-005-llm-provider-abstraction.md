---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/application/interfaces/llm/llm_provider.py`, `src/platformmind/infrastructure/llm/groq_provider.py`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# ADR-005: LLM Provider Abstraction

## Purpose
This document records the decision to abstract the LLM provider instead of coupling directly to a specific vendor (e.g., Groq, OpenAI).

## Responsibilities
Provides a uniform interface for text generation and reasoning tasks regardless of the underlying model.

## Location in Codebase
- `src/platformmind/application/interfaces/llm/llm_provider.py`
- `src/platformmind/infrastructure/llm/`

## Related Modules
- [Application Layer](../architecture/APPLICATION_LAYER.md)
- [Adding an LLM Provider](../development/ADDING_LLM_PROVIDER.md)

## Dependencies
Currently depends on the Groq SDK (`GroqProvider`), but the application core depends only on `LLMProvider`.

## Internal Workflow
The Planner and Learning Engine request generation from the `LLMProvider` interface. The injected adapter translates this into vendor-specific API calls.

## Input
System prompts, user instructions, configuration (temperature, max tokens).

## Output
Generated text strings or structured JSON outputs.

## Error Handling
Vendor-specific rate limits and API errors are wrapped in domain `PlatformMindException` types.

## Performance Notes
Groq was chosen as the default implementation for its high-speed inference, which is critical for the recursive Capability Synthesis loop.

## Extension Points
New providers (e.g., OpenAI, Anthropic) can be added simply by implementing `LLMProvider`.

## Current Limitations
- Token usage tracking is not yet unified across different provider adapters.

## Future Improvements
- Implement automatic fallback to secondary providers upon primary provider failure.
