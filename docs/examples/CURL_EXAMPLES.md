---
Last Updated: 2026-07-26
Related Source Files: N/A
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# cURL Examples

## Purpose
How to interact with the API via terminal.

## Execute a Task
```bash
curl -X POST http://localhost:8000/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "instruction": "Create a bug issue for the missing index in the users table",
    "context": {
      "repository": "owner/platformmind"
    }
  }'
```

## Check Memory Context
```bash
curl -X GET "http://localhost:8000/api/v1/memory?limit=5"
```

## Get an Execution Report
```bash
curl -X GET http://localhost:8000/api/v1/reports/123e4567-e89b-12d3-a456-426614174000
```
