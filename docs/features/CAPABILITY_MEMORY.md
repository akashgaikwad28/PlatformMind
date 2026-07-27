---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/application/memory/services/capability.py`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Capability Memory

## Purpose
Explains how the system stores and reuses known tool sequences.

## Responsibilities
Preventing the planner from hallucinating new execution plans for tasks it already knows how to do.

## Location in Codebase
- `src/platformmind/application/memory/services/capability.py`

## Related Modules
- [Runtime Synthesis](RUNTIME_SYNTHESIS.md)
- [Memory System](MEMORY_SYSTEM.md)

## Dependencies
`CapabilityRepository`.

## Internal Workflow
When a task is successfully executed, its DAG is hashed and stored as a `Capability`. Future instructions matching the intent of that capability will reuse the exact same DAG structure, skipping the LLM decomposition phase entirely.

## Input
`ExecutionPlan`, `Instruction`.

## Output
`Capability` entity.

## Error Handling
N/A

## Performance Notes
Fetching a capability reduces Planning time from ~3 seconds (LLM inference) to ~0.05 seconds (DB lookup).

## Extension Points
N/A

## Current Limitations
- Parameter matching. A capability built for "Create issue in Repo A" must be abstracted to "Create issue in Repo X" to be reusable.

## Future Improvements
- Better AST-based abstraction of capability parameters.
