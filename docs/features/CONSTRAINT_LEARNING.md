---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/application/learning/`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Constraint Learning

## Purpose
Allows the agent to remember environmental rules (like branch protections) to avoid repeating mistakes.

## Responsibilities
Parsing error messages to extract declarative rules.

## Location in Codebase
- `src/platformmind/application/learning/`

## Related Modules
- [Learning Engine](LEARNING.md)

## Dependencies
LLM Provider.

## Internal Workflow
If an API call fails with a 403 or 422, the error message and the attempted API payload are passed to the LLM with a prompt to extract the constraint. For example, "Repository X requires signed commits." This rule is then saved to `ConstraintMemoryService`.

## Input
Failed API payloads and error responses.

## Output
`Constraint` domain model.

## Error Handling
If the LLM cannot extract a clear constraint, it aborts rather than storing a hallucination.

## Performance Notes
Requires an extra LLM call post-execution.

## Extension Points
N/A

## Current Limitations
- Constraints are sometimes too specific to a single execution context.

## Future Improvements
- Periodically use the LLM to merge and generalize constraints.
