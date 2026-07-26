---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/domain/exceptions/`, `src/platformmind/api/exception_handlers.py`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Error Codes

## Purpose
Reference for standard API error schemas.

## Standard Error Response Schema
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE_STRING",
    "message": "Human readable message",
    "details": {},
    "request_id": "uuid-for-tracing"
  }
}
```

## Common Error Codes

| HTTP Status | Error Code | Description |
| --- | --- | --- |
| `400` | `VALIDATION_ERROR` | Malformed JSON or failed Pydantic validation. |
| `400` | `INVALID_INSTRUCTION` | NLP instruction is empty or unparseable. |
| `404` | `NOT_FOUND` | Resource (e.g. execution_id) not found. |
| `429` | `PLATFORM_RATE_LIMIT` | Target platform (e.g. GitHub) returned a 429. |
| `500` | `INTERNAL_ERROR` | Unhandled exception inside PlatformMind. |
| `502` | `LLM_PROVIDER_ERROR` | Groq or LLM provider failed. |

## Handling
All these are mapped automatically by the `platformmind_exception_handler` in `src/platformmind/api/exception_handlers.py`.
