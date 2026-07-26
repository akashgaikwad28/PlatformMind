---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/application/planner/`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Planner Module

## Purpose
The Planner is responsible for translating a natural language instruction into a directed acyclic graph (DAG) of executable tools.

## Responsibilities
- Context resolution and instruction normalization.
- Memory retrieval to augment planning prompts.
- Tool selection from the registry.
- Task decomposition and dependency mapping.
- Capability matching.

## Location in Codebase
- `src/platformmind/application/planner/`

## Related Modules
- [Planner Architecture](../architecture/PLANNER_ARCHITECTURE.md)
- [Tool Selection Feature](../features/TOOL_SELECTION.md)

## Dependencies
Depends on `MemoryEngine` (for context), `LLMProvider` (for reasoning), and `ToolRegistry` (for operations).

## Internal Workflow
The process follows a strict pipeline defined in `PlanningPipeline`:
1. `InstructionNormalizer`
2. `IntentClassifier`
3. Memory Retrieval
4. `CapabilityMatcher`
5. `TaskDecomposer`
6. `ToolSelector`
7. `DependencyResolver`
8. `ExecutionPlanBuilder`
9. `ExecutionPlanValidator`

## Input
Raw `Instruction`.

## Output
Validated `ExecutionPlan` containing `ExecutionStep` sequences.

## Error Handling
Validation failures in the pipeline trigger a fallback to `CapabilitySynthesizer`. If synthesis fails, an exception is thrown.

## Performance Notes
The LLM inference in the `TaskDecomposer` is the slowest component. Memory augmented retrieval significantly reduces required prompt size and speeds up planning.

## Extension Points
New pipeline stages can be added by implementing the required interface and injecting it into the `PlanningPipeline`.

## Current Limitations
- Complex tasks occasionally fail to resolve deeply nested dependencies correctly in a single pass.

## Future Improvements
- Multi-step, iterative planning (ReAct) for complex DAG resolution.
