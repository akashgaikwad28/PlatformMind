---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/application/reporting/`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Execution Reports

## Purpose
Explains how the system provides observability into its operations.

## Responsibilities
Transforming raw `ExecutionResult` objects into human-readable Markdown and machine-readable JSON reports.

## Location in Codebase
- `src/platformmind/application/reporting/`

## Related Modules
- [Report Generation](REPORT_GENERATION.md)
- [Reports Endpoint](../api/REPORTS_ENDPOINT.md)

## Dependencies
`ReportRepository`.

## Internal Workflow
After an execution completes, the API Layer requests the `ReportingEngine` to format the result. It generates a markdown summary of what steps were taken, what tools were used, how long they took, and what the ultimate success status was.

## Input
`ExecutionResult`.

## Output
`ExecutionReport`.

## Error Handling
Report generation errors must not fail the original API request.

## Performance Notes
Reports are generated synchronously after execution.

## Extension Points
New report formats (e.g. HTML) can be added to the `ExecutionReporter` interface.

## Current Limitations
- Markdown reports do not include syntax highlighting for tool payload JSON.

## Future Improvements
- Stream execution report logs in real-time.
