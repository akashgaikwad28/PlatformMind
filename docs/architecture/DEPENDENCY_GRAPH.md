---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/api/container.py`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Dependency Graph

## Purpose
This document visualizes and explains the dependency injection (DI) strategy used in PlatformMind.

## Responsibilities
- Managing object lifecycles.
- Wiring Infrastructure implementations to Application interfaces.

## Location in Codebase
- `src/platformmind/api/container.py`
- `src/platformmind/api/dependencies.py`

## Related Modules
- [Clean Architecture](CLEAN_ARCHITECTURE.md)
- [API Layer](API_LAYER.md)

## Dependencies
FastAPI's built-in `Depends` system for HTTP injection.

## Internal Workflow
The `setup_container` function initializes singletons (like DB connections and LLM clients) and constructs the primary application services (`ExecutionOrchestrator`, `PlanningPipeline`, `MemoryEngineImpl`). These are cached and injected into API routes.

```python
# Example of DI wiring in container.py
llm_provider = GroqProvider(api_key=settings.GROQ_API_KEY)
planner = PlannerImpl(llm_provider=llm_provider, tool_registry=registry)
```

## Input
Configuration from environment variables.

## Output
Instantiated service classes.

## Error Handling
Missing configurations raise immediate validation errors at startup, preventing the server from running in a broken state.

## Performance Notes
Most services are instantiated as singletons on application startup to avoid instantiation overhead on every request.

## Extension Points
To inject a new service, instantiate it in `container.py` and yield it via a new dependency function in `dependencies.py`.

## Current Limitations
- Using manual DI rather than a framework like `dependency-injector`, which can make `container.py` verbose.

## Future Improvements
- Refactor to use a formal DI framework if the dependency graph becomes too deeply nested.
