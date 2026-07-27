---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/api/routers/`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# API Reference

## Purpose
This document serves as the index for the PlatformMind REST API endpoints.

## Base URL
All v1 endpoints are prefixed with `/api/v1`.

## Endpoints

| Endpoint | Method | Description | Link |
| --- | --- | --- | --- |
| `/api/v1/execute` | `POST` | Execute a natural language instruction. | [Execute](EXECUTE_ENDPOINT.md) |
| `/api/v1/capabilities` | `GET` | Retrieve registered and synthesized capabilities. | [Capabilities](CAPABILITIES_ENDPOINT.md) |
| `/api/v1/memory` | `GET` | View the operational memory context. | [Memory](MEMORY_ENDPOINT.md) |
| `/api/v1/metrics` | `GET` | Fetch system learning metrics. | [Metrics](METRICS_ENDPOINT.md) |
| `/api/v1/reports` | `GET` | Retrieve structured execution reports. | [Reports](REPORTS_ENDPOINT.md) |

## Common Models

### `APIResponse`
All successful endpoints wrap their payload in a standard envelope: "```json"
{
  "success": true,
  "data": { ... }
}
```

### `APIErrorResponse`
See [Error Codes](ERROR_CODES.md) for detailed schemas and handling of failed requests.

## Authentication
> **Not implemented yet.**
> Currently, the API runs locally without API key authentication. Ensure it is not exposed directly to the public internet without a reverse proxy.
