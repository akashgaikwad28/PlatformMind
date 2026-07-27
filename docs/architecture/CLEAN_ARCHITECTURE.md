---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/domain`, `src/platformmind/application`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Clean Architecture

## Purpose
This document explains the strict enforcement of Clean Architecture principles within PlatformMind.

## Responsibilities
Ensuring that business rules (Domain and Application layers) remain completely isolated from UI, database, and third-party API dependencies.

## Location in Codebase
Enforced via the directory structure:
- `src/platformmind/domain/` (Inner circle)
- `src/platformmind/application/` (Use cases)
- `src/platformmind/api/` (Outer circle - UI/Presentation)
- `src/platformmind/infrastructure/` (Outer circle - DB/External)

## Related Modules
- [ADR-001 Adoption of Clean Architecture](../adr/ADR-001-clean-architecture.md)
- [Domain Model](DOMAIN_MODEL.md)

## Dependencies
The Dependency Rule is strictly followed: source code dependencies can only point *inward*.

## Internal Workflow
The `Application` layer defines `Interfaces` (ports) for things it needs (e.g., `ExecutionRepository`). The `Infrastructure` layer implements these interfaces (adapters). The `API` layer wires the adapters to the application services via a Dependency Injection container.

## Input
N/A

## Output
N/A

## Error Handling
Infrastructure exceptions (like `sqlalchemy.exc.OperationalError`) must be caught and translated into `PlatformMindException` types before crossing the boundary into the Application layer.

## Performance Notes
Dependency inversion introduces minimal overhead, ensuring testability via mocks.

## Extension Points
Any outer-circle technology can be swapped out (e.g., SQLite to PostgreSQL, or FastAPI to a CLI) without changing a single line of code in the Application or Domain layers.

## Current Limitations
- Increases the number of files and boilerplate (interfaces + implementations).

## Future Improvements
- Add automated architectural tests to fail CI if an inner layer imports from an outer layer.
