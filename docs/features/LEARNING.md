---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/application/learning/analyzer.py`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Learning Engine

## Purpose
The Learning Engine is the mechanism by which PlatformMind improves its success rate over time.

## Responsibilities
Evaluating past executions to tune capability scores and extract constraints.

## Location in Codebase
- `src/platformmind/application/learning/analyzer.py`

## Related Modules
- [Learning Loop Diagram](../diagrams/learning-loop.md)
- [Learning Architecture](../architecture/LEARNING_ENGINE.md)
- [Constraint Learning](CONSTRAINT_LEARNING.md)

## Dependencies
Memory Engine.

## Internal Workflow
When an execution finishes, `ExecutionAnalyzer.analyze()` is called. It calculates the moving average success rate of the tools used and the overall capability. If it detects a failure caused by the platform (e.g., branch protection rules), it delegates to the Constraint extractor.

## Input
`ExecutionResult`

## Output
Updated memory models.

## Error Handling
Fails safely, meaning learning failure does not corrupt the actual execution record.

## Performance Notes
Running post-execution ensures it does not impact API response time (if run asynchronously).

## Extension Points
New analysis algorithms can be added to the analyzer pipeline.

## Current Limitations
- Success rates are global, not repository-specific.

## Future Improvements
- Multi-dimensional success tracking (e.g. per-repo, per-user).
