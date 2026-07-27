---
Last Updated: 2026-07-26
Related Source Files: "`tests/`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Testing Guide

## Purpose
Defines the testing strategy and standards for PlatformMind.

## Responsibilities
Ensuring code correctness across all boundaries.

## Location in Codebase
- `tests/`

## Related Modules
- [Clean Architecture](../architecture/CLEAN_ARCHITECTURE.md)

## Dependencies
`pytest`, `pytest-asyncio`.

## Internal Workflow

### Test Strategy
PlatformMind relies on the testing pyramid:
1. **Unit Tests (`tests/unit/`)**: Test pure domain models and application use cases using mocks. Fast, isolated, no DB.
2. **Integration Tests (`tests/integration/`)**: Test `infrastructure/` adapters against real external systems (or local Docker instances of them, like a test DB).
3. **End-to-End Tests (`tests/e2e/`)**: Test the full API flow via `TestClient`.

### Mock Strategy
Mocks are strictly typed using `unittest.mock.MagicMock` but wrapped in strongly typed helper classes in `tests/mocks/` to ensure interfaces match `application/interfaces/`. Never mock what you do not own.

### Coverage
Target coverage is 85%. Enforced via `pytest-cov` in CI.

## Input
N/A

## Output
Test reports.

## Error Handling
Flaky tests (especially against live GitHub API endpoints) must be marked with `@pytest.mark.flaky`.

## Performance Notes
Run unit tests with `uv run pytest tests/unit -n auto` for parallel execution.

## Extension Points
Add new fixtures in `tests/fixtures/conftest.py`.

## Current Limitations
- Integration tests against GitHub require a dedicated test account token, otherwise rate limits break CI.

## Future Improvements
- Implement VCR.py to record and replay HTTP requests for deterministic infrastructure tests.
