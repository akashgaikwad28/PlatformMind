---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/api/routers/v1/capabilities.py`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Capabilities Endpoint

## Purpose
List all available workflows (including built-in and dynamically synthesized capabilities).

## Route
`GET /api/v1/capabilities`

## Request Model
None.

## Response Model
Defined in `CapabilityResponse`.
```json
{
  "success": true,
  "data": {
    "capabilities": [
      {
        "id": "uuid",
        "intent": "Create Issue",
        "success_rate": 0.98,
        "is_synthesized": false
      }
    ]
  }
}
```

## Execution Flow
Delegates to `CapabilityMemoryService.get_all()`.

## Error Codes
- `500 Internal Server Error`

## Related Services
- `CapabilityMemoryService`
