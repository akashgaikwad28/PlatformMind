---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/api/routers/v1/reports.py`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Reports Endpoint

## Purpose
Retrieve structured execution reports for past instructions.

## Route
`GET /api/v1/reports/{execution_id}`

## Request Model
Path Parameters:
- `execution_id` (UUID): The ID of the execution.

## Response Model
Defined in `ExecutionReportResponse`.
```json
{
  "success": true,
  "data": {
    "execution_id": "uuid",
    "report_markdown": "# Execution Report...",
    "report_json": { ... }
  }
}
```

## Execution Flow
Delegates to `ReportingEngineImpl.get_report()`. If the report is not cached, it fetches the raw execution from `ExecutionRepositoryImpl` and generates the report on the fly.

## Error Codes
- `404 Not Found`: Execution ID not found.

## Related Services
- `ReportingEngine`
