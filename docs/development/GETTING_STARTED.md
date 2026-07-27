---
Last Updated: 2026-07-26
Related Source Files: "`Makefile`, `pyproject.toml`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Getting Started

## Purpose
Guide new developers through setting up PlatformMind locally.

## Responsibilities
Environment setup, dependency installation, and local execution.

## Location in Codebase
N/A

## Related Modules
- [Environment Variables](ENVIRONMENT_VARIABLES.md)
- [Testing Guide](TESTING_GUIDE.md)

## Dependencies
Python 3.13+, `uv`.

## Internal Workflow
1. Clone the repository.
2. Install `uv`.
3. Run `uv sync`.
4. Copy `.env.example` to `.env` and populate credentials.
5. Run migrations via `alembic upgrade head` (if necessary, though SQLite auto-creates in dev).
6. Start the server.

## Input
N/A

## Output
Running FastAPI instance on `localhost:8000`.

## Error Handling
Refer to [Startup Errors](../troubleshooting/STARTUP_ERRORS.md) if the server crashes on boot.

## Performance Notes
Using `uv` guarantees near-instant dependency resolution.

## Extension Points
N/A

## Current Limitations
- Windows support is provided via WSL2 for some CLI tools (like make).

## Future Improvements
- Provide a `docker-compose.yml` that mounts the local directory for zero-install development.
