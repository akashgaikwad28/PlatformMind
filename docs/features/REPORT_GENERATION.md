---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/application/reporting/engine.py`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Report Generation

## Purpose
Deep dive into the templating of Execution Reports.

## Responsibilities
Formatting data.

## Location in Codebase
- `src/platformmind/application/reporting/engine.py`

## Related Modules
- [Execution Reports](EXECUTION_REPORTS.md)
- [Execution Report Generation Diagram](../diagrams/execution-report-generation.md)

## Dependencies
Standard library strings.

## Internal Workflow
Iterates over the `ExecutionPlan` steps and matches them with `ExecutionMetrics` from the `ExecutionResult`. Creates a table of executed tools, their duration, and success status.

## Input
`ExecutionResult`.

## Output
String (Markdown).

## Error Handling
N/A

## Performance Notes
Instantaneous string concatenation.

## Extension Points
Jinja2 could be injected if templates become highly complex.

## Current Limitations
- Hardcoded markdown templates in python strings.

## Future Improvements
- Move templates to `.j2` files.
