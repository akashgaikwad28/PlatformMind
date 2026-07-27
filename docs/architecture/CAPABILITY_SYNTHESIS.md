---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/application/planner/pipeline.py`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Capability Synthesis Architecture

## Purpose
Explains how the agent creates missing capabilities at runtime.

## Responsibilities
Generating new DAGs for unknown intents.

## Location in Codebase
- Fallback branch in `src/platformmind/application/planner/pipeline.py`.

## Related Modules
- [Capability Synthesis Diagram](../diagrams/capability-synthesis.md)

## Dependencies
LLM Provider, Tool Registry.

## Internal Workflow
If `CapabilityMatcher` fails, the `TaskDecomposer` asks the LLM to invent a sequence. If it executes successfully once, it is promoted to a registered `Capability` in memory.

## Input
Unknown instructions.

## Output
New synthesized capabilities.

## Error Handling
Reverts safely if the synthesis causes damage (via rollback).

## Performance Notes
Very slow (requires LLM reasoning + sandbox trial execution).

## Extension Points
N/A

## Current Limitations
- Sandbox execution currently runs against live repositories; rollback is not always 100% perfect.

## Future Improvements
- True sandboxing using isolated test repositories before committing capabilities to memory.
