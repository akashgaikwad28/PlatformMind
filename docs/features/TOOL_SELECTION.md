---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/application/planner/tool_selector.py`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Tool Selection

## Purpose
Explains how the planner decides which tools to use.

## Responsibilities
Filtering the massive `ToolRegistry` down to only the tools relevant to the current `Instruction`.

## Location in Codebase
- `src/platformmind/application/planner/tool_selector.py`

## Related Modules
- [Tool Selection ADR](../adr/ADR-003-tool-selection.md)

## Dependencies
ToolRegistry.

## Internal Workflow
1. The `Instruction` intent is extracted.
2. The `ToolSelector` calculates a relevance score for every registered tool based on its docstring and parameter schema against the intent.
3. Top N tools are passed to the `TaskDecomposer` LLM prompt to reduce token context size.

## Input
Intent string, Tool Registry.

## Output
List of `BaseTool` references.

## Error Handling
If no tools match above the threshold, an empty list is returned, forcing Capability Synthesis.

## Performance Notes
Uses basic TF-IDF or fast embeddings.

## Extension Points
N/A

## Current Limitations
- Relies heavily on developers writing extremely clear docstrings for their tools.

## Future Improvements
- Allow the LLM to search the tool registry iteratively.
