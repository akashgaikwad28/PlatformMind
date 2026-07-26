---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Troubleshooting Index

## Purpose
Directory for operational and runtime issues.

## Categories

### Application Issues
- [Startup Errors](STARTUP_ERRORS.md)
- [Database & Memory Problems](DATABASE_PROBLEMS.md)

### External Dependencies
- [Authentication & Rate Limits](AUTHENTICATION_ERRORS.md)

### Agent Logic
- [Debugging the Planner](DEBUGGING_PLANNER.md)

## First Steps
If you encounter an issue not listed here:
1. Set `LOG_LEVEL=DEBUG` in `.env`.
2. Inspect the API response's `error.details` array.
3. Check the `ExecutionReport` (via the `/reports` endpoint) for the exact payload that failed.
