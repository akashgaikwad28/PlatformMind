---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Design Decisions

## Purpose
Consolidates the reasoning behind major architectural choices.

## Responsibilities
Providing context for engineering decisions.

## Location in Codebase
N/A

## Related Modules
- [Architecture Decision Records (ADRs)](../adr/)

## Dependencies
N/A

## Internal Workflow
N/A

## Input
N/A

## Output
N/A

## Error Handling
N/A

## Performance Notes
N/A

## Extension Points
N/A

## Current Limitations
N/A

## Future Improvements
N/A

## Summary of Key Decisions
- **Why Clean Architecture?** To ensure the core capability synthesis and planning logic can be tested and evolved without breaking the API or being locked into a specific database. (See ADR-001)
- **Why SQLite?** Zero-configuration setup is crucial for developer experience. The abstraction allows swapping to Postgres later.
- **Why ChromaDB?** It runs in-process locally, meaning zero latency network calls for memory retrieval, which is essential for rapid planning. (See ADR-004)
- **Why FastAPI?** Native async support and built-in OpenAPI schema generation, which is required for integrations.
- **Why Dependency Injection?** To easily inject mock LLM providers and GitHub clients during the extensive integration test suite.
- **Why Planner Pipeline?** To decompose the complex prompt into smaller, focused LLM calls. This increases accuracy and reduces hallucinations compared to one massive "do everything" prompt.
