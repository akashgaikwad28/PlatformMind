---
Last Updated: 2026-07-26
Related Source Files: `ruff.toml`, `mypy.ini`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Coding Standards

## Purpose
Ensures consistent style and safety across the repository.

## Responsibilities
Linting, type checking, and formatting.

## Location in Codebase
- `ruff.toml`
- `mypy.ini`

## Related Modules
- [Testing Guide](TESTING_GUIDE.md)

## Dependencies
`ruff`, `mypy`.

## Internal Workflow
Code must pass:
1. `uv run ruff check .`
2. `uv run ruff format --check .`
3. `uv run mypy src`

## Input
Source code.

## Output
Zero exit codes in CI.

## Error Handling
Violations break the build.

## Performance Notes
Ruff executes in milliseconds.

## Extension Points
Modify rules in `.toml` files.

## Current Limitations
- `Any` types are still permitted in some infrastructure adapters dealing with raw JSON.

## Future Improvements
- Enable `strict = true` in Mypy globally.
