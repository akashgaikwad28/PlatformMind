---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/application/memory/engine.py`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Memory System

## Purpose
Explains the overarching design of PlatformMind's contextual memory.

## Responsibilities
Serving as the central hub that integrates Capabilities, Constraints, and Executions into a unified context payload for the Planner.

## Location in Codebase
- `src/platformmind/application/memory/engine.py`

## Related Modules
- [Capability Memory](CAPABILITY_MEMORY.md)
- [Execution Memory](EXECUTION_MEMORY.md)
- [Memory Retrieval](MEMORY_RETRIEVAL.md)
- [Constraint Learning](CONSTRAINT_LEARNING.md)

## Dependencies
ChromaDB, SQLite.

## Internal Workflow
The `MemoryEngineImpl` facade exposes `get_context(instruction)`. It fans out requests to the three specialized memory services (`CapabilityMemoryService`, `ExecutionMemoryService`, `ConstraintMemoryService`).

## Input
Raw natural language `Instruction`.

## Output
Ranked `MemoryContext` object.

## Error Handling
Graceful degradation. If the VectorDB is unavailable, it falls back to a zero-memory state.

## Performance Notes
Asynchronous fan-out allows fetching from ChromaDB and SQLite concurrently.

## Extension Points
New memory subtypes can be added by implementing a new `MemoryService`.

## Current Limitations
- Memory context can grow very large for complex prompts, risking LLM token limits.

## Future Improvements
- Implement a more aggressive summarization phase in the `MemoryCompactor`.
