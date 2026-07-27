---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/api/routers/v1/execution.py`, `src/platformmind/api/schemas/requests.py`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Execute Endpoint

## Purpose
Submit a natural language instruction for the agent to process and execute against the target platform.

## Route
`POST /api/v1/execute`

## Request Model
Defined in `ExecuteRequest`.
```json
{
  "instruction": "Create a new issue about a bug in the auth module",
  "context": {
    "repository": "owner/repo"
  }
}
```

## Validation Rules
- `instruction`: Required, non-empty string.
- `context`: Optional dictionary of key-value pairs providing environmental context.

## Response Model
Defined in `ExecutionReportResponse`.
```json
{
  "success": true,
  "data": {
    "execution_id": "uuid-string",
    "status": "COMPLETED",
    "plan_id": "uuid-string",
    "steps_executed": 1,
    "metrics": {
      "duration_ms": 1250.0,
      "api_calls": 1
    }
  }
}
```

## Execution Flow
See the [Request Lifecycle](../architecture/REQUEST_LIFECYCLE.md).

## Error Codes
- `400 Bad Request`: Validation failure or Invalid Instruction.
- `500 Internal Server Error`: Unhandled platform exception.
See [Error Codes](ERROR_CODES.md).

## Example Request
See [cURL Examples](../examples/CURL_EXAMPLES.md).

## Related Services
- `ExecutionOrchestrator`
- `PlanningPipeline`
