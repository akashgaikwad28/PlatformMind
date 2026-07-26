---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/application/execution/`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Execution Lifecycle

## Purpose
Explains the state machine of an execution.

## Responsibilities
Tracking the exact status of a run.

## Location in Codebase
- `src/platformmind/application/execution/state_manager.py`

## Related Modules
- [Execution Engine Architecture](../architecture/EXECUTION_ENGINE.md)
- [State Machine Diagram](../diagrams/state-machine.md)

## Dependencies
None.

## Internal Workflow
Executions move from `PENDING` -> `RUNNING`. Individual steps move through `READY` -> `EXECUTING` -> `SUCCESS`/`FAILED`.
If a step fails, it can loop through `RETRYING` until exhaustion.
If the DAG completes, it hits `COMPLETED`. If a fatal error occurs, it goes to `ROLLING_BACK` and then `FAILED`.

## Input
State transition events.

## Output
Current `ExecutionStatus`.

## Error Handling
Invalid state transitions raise `InvalidStateError`.

## Performance Notes
N/A

## Extension Points
N/A

## Current Limitations
- Cannot pause and resume an execution from persistent storage.

## Future Improvements
- Persist state transitions to the database to survive server restarts.
