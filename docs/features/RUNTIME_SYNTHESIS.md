---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/application/planner/pipeline.py`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Runtime Synthesis

## Purpose
Ensures the agent never fails silently when asked to do something it doesn't currently know how to do.

## Responsibilities
Dynamically generating, testing, and saving new workflows.

## Location in Codebase
- `src/platformmind/application/planner/pipeline.py`

## Related Modules
- [Capability Synthesis Architecture](../architecture/CAPABILITY_SYNTHESIS.md)
- [Capability Synthesis Example](../examples/CAPABILITY_SYNTHESIS.md)

## Dependencies
LLM Provider, Tool Registry.

## Internal Workflow
See [Capability Synthesis Diagram](../diagrams/capability-synthesis.md).
The Planner delegates to the Synthesizer when no matching capability is found. The LLM guesses a DAG, it runs in a sandbox, and if successful, the DAG is committed to memory as a new Capability.

## Input
Unknown intent string.

## Output
New `Capability`.

## Error Handling
If synthesis fails after max retries, it throws an `UnsupportedInstructionError`.

## Performance Notes
Extremely high latency. Expected to take >10 seconds.

## Extension Points
N/A

## Current Limitations
- The sandbox is not completely isolated.

## Future Improvements
- True ephemeral sandboxes (e.g. test repos) for synthesis trials.
