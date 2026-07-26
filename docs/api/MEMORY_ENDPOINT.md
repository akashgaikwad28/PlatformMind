---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/api/routers/v1/memory.py`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Memory Endpoint

## Purpose
Inspect the current state of operational memory.

## Route
`GET /api/v1/memory`

## Request Model
Query Parameters (Optional):
- `limit` (int): Number of records to return. Default 10.
- `type` (string): Filter by memory type (`execution`, `constraint`, `capability`).

## Response Model
Defined in `MemoryResponse`.
```json
{
  "success": true,
  "data": {
    "records": [
      {
        "id": "uuid-string",
        "type": "constraint",
        "content": "Cannot create branches without issue reference."
      }
    ]
  }
}
```

## Execution Flow
The router calls `MemoryEngineImpl.get_all()` mapping across the different memory stores.

## Error Codes
- `500 Internal Server Error`: Database connection failure.

## Related Services
- `MemoryEngine`
