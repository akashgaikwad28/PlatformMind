---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/application/planner/pipeline.py`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Planner

## Purpose
The Planner is the brain of the operation, converting NLP to DAGs.

## Responsibilities
Resolving dependencies between steps (e.g., getting a Repo ID before creating an Issue).

## Location in Codebase
- `src/platformmind/application/planner/`

## Related Modules
- [Planner Architecture](../architecture/PLANNER_ARCHITECTURE.md)
- [Tool Selection](TOOL_SELECTION.md)

## Dependencies
LLM Provider, Memory Engine.

## Internal Workflow
See [Planner Flow](../diagrams/planner-flow.md).

## Input
Instruction, Context.

## Output
ExecutionPlan.

## Error Handling
Syntax errors from the LLM (e.g. malformed JSON) trigger automatic retries within the `TaskDecomposer`.

## Performance Notes
Latency heavily depends on the LLM provider.

## Extension Points
N/A

## Current Limitations
- The LLM can sometimes generate circular dependencies in the DAG.

## Future Improvements
- Add strict DAG circular dependency validation before passing to the Execution Engine.
