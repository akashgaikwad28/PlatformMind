---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/application/learning/`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Learning Engine Architecture

## Purpose
Explains how PlatformMind improves over time.

## Responsibilities
Analyzing executions and updating capability success rates and constraints.

## Location in Codebase
- `src/platformmind/application/learning/`

## Related Modules
- [Learning Loop Diagram](../diagrams/learning-loop.md)

## Dependencies
Memory Engine.

## Internal Workflow
Applies Exponential Moving Average (EMA) to tool and capability success rates. Extracts error logs to form declarative constraints.

## Input
`ExecutionResult`.

## Output
Updated `Capability` and `Constraint` models.

## Error Handling
Fails silently so as not to crash the main API response if learning fails.

## Performance Notes
Runs asynchronously.

## Extension Points
Add new analyzer strategies.

## Current Limitations
- EMA can be slow to adapt if early failures were due to transient external issues.

## Future Improvements
- Add context-aware learning metrics (e.g. success rate *per repository*).
