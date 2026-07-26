---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/core/config/`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Troubleshooting Startup Errors

## Purpose
Resolve issues encountered when booting the FastAPI application.

## Common Symptoms
The application crashes immediately after running `uv run uvicorn src.platformmind.api.app:app`.

## ValidationErrors
```
pydantic_core._pydantic_core.ValidationError: 2 validation errors for Settings
```
**Cause:** Missing environment variables.
**Resolution:** Ensure `.env` exists and contains `GROQ_API_KEY` and `GITHUB_TOKEN`. See [Environment Variables](../development/ENVIRONMENT_VARIABLES.md).

## Address already in use
```
[Errno 98] Address already in use
```
**Cause:** Port 8000 is occupied.
**Resolution:** Kill the conflicting process or run `uvicorn` with `--port 8080`.

## ModuleNotFoundError
```
ModuleNotFoundError: No module named 'platformmind'
```
**Cause:** Python path is not set correctly, or dependencies are out of sync.
**Resolution:** Ensure you are running commands via `uv run` and that `uv sync` has been run successfully.
