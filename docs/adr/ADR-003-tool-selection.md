---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/application/execution/tool_registry.py`, `src/platformmind/application/planner/tool_selector.py`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# ADR-003: Dynamic Tool Selection

## Purpose
This document records the decision to use dynamic tool selection via the Planner rather than hardcoded workflows.

## Responsibilities
The Planner dynamically constructs Execution Plans by selecting tools from a registered pool based on the instruction and context.

## Location in Codebase
- `src/platformmind/application/planner/tool_selector.py`
- `src/platformmind/application/execution/tool_registry.py`

## Related Modules
- [Planner Architecture](../architecture/PLANNER_ARCHITECTURE.md)
- [Tool Selection](../features/TOOL_SELECTION.md)

## Dependencies
Depends on the LLM Provider for reasoning and the Tool Registry for available operations.

## Internal Workflow
The Planner matches the intent of the instruction against descriptions of available tools, scoring them based on semantic fit and historical success rates, before generating the execution sequence.

## Input
Instruction context and Capability Memory.

## Output
Directed Acyclic Graph (DAG) of selected tools.

## Error Handling
If no suitable tools are found, the system delegates to Capability Synthesis.

## Performance Notes
Tool selection happens at planning time; execution is unaffected by selection latency.

## Extension Points
Developers can add new tools by inheriting from `BaseTool` and registering them in the `ToolRegistry`.

## Current Limitations
- Complex tasks occasionally select incorrect tools due to ambiguous descriptions.

## Future Improvements
- Improve tool descriptions using execution-driven feedback.
