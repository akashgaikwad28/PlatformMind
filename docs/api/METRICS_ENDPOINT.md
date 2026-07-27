---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/api/routers/v1/metrics.py`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Metrics Endpoint

## Purpose
View system-wide performance and learning improvements.

## Route
`GET /api/v1/metrics`

## Request Model
None.

## Response Model
Defined in `MetricResponse`.
```json
{
  "success": true,
  "data": {
    "total_executions": 150,
    "success_rate": 0.95,
    "synthesized_capabilities": 12
  }
}
```

## Execution Flow
Delegates to `LearningEngine` to compile aggregates.

## Error Codes
- `500 Internal Server Error`

## Related Services
- `LearningEngine`
