---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/application/memory/`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Memory Architecture

## Purpose
Explains the segmented knowledge storage system.

## Responsibilities
Providing the Planner with the precise context needed to succeed, drawn from past experience.

## Location in Codebase
- `src/platformmind/application/memory/`

## Related Modules
- [Memory Flow Diagram](../diagrams/memory-flow.md)
- [Memory Module](../memory/README.md)

## Dependencies
ChromaDB, SQLite.

## Internal Workflow
Memory is split into capability memory (tools), execution memory (past outcomes), and constraint memory (rules). They are fetched concurrently, ranked, and injected into the Planner prompt.

## Input
Execution outcomes.

## Output
Memory payload.

## Error Handling
Fail-open architecture. If memory retrieval fails, planning proceeds with zero context.

## Performance Notes
Semantic search via ChromaDB is very fast locally.

## Extension Points
Implement new `MemoryService` interfaces.

## Current Limitations
- Embeddings are generated per request, taking some time.

## Future Improvements
- Cache common embeddings.
