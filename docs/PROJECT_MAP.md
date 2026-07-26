---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind`, `tests`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Project Map

## Purpose
This document provides a comprehensive view of the PlatformMind repository structure. It explains the responsibility of every top-level directory and core package to help developers orient themselves in the codebase.

## Repository Tree

```text
PlatformMind/
├── .github/                  # GitHub Actions CI/CD workflows
├── docs/                     # Project documentation system
├── src/
│   └── platformmind/
│       ├── api/              # FastAPI presentation layer
│       ├── application/      # Use cases, orchestration, and business logic
│       ├── cli/              # Command-line interfaces and scripts
│       ├── core/             # Core utilities, configuration, and settings
│       ├── domain/           # Domain models, entities, and business rules
│       ├── infrastructure/   # External integrations (Database, LLMs, GitHub)
│       ├── prompts/          # System prompts for LLM integrations
│       └── services/         # Cross-cutting application services
├── tests/
│   ├── e2e/                  # End-to-end API tests
│   ├── fixtures/             # Reusable pytest fixtures
│   ├── integration/          # Integration tests for external boundaries
│   ├── mocks/                # Mock implementations of interfaces
│   └── unit/                 # Isolated unit tests for domain and application logic
├── .env.example              # Template for environment variables
├── pyproject.toml            # Python project metadata and dependencies
├── ruff.toml                 # Ruff linter/formatter configuration
├── mypy.ini                  # Static type checking configuration
├── alembic.ini               # Database migration configuration
├── Makefile                  # Developer workflow automation
└── README.md                 # Primary project entrypoint
```

## Package Responsibilities

### `src/platformmind/api`
The HTTP entry point into the system. Built with FastAPI. It defines routes, request/response DTOs, dependency injection mapping (`container.py`), and error handling middleware. 
- **Entry Point:** `app.py` (FastAPI app factory)
- **Key Files:** `routers/v1/execution.py`, `container.py`

### `src/platformmind/application`
The Application layer orchestrates the domain models to accomplish specific use cases. It contains the primary engines of the system:
- **Planner (`application/planner/`):** Decomposes natural language into execution plans.
- **Execution (`application/execution/`):** Executes plans using the tool registry, handles retries, and records metrics.
- **Memory (`application/memory/`):** Services for managing capabilities, executions, and constraints.
- **Learning (`application/learning/`):** Evaluates executions to improve future metrics.
- **Interfaces (`application/interfaces/`):** Defines ports that the infrastructure layer implements, strictly enforcing Clean Architecture dependency inversion.

### `src/platformmind/domain`
The core business rules. This package has **zero dependencies** on external libraries (other than standard library/Pydantic).
- **Models:** Entities like `Instruction`, `ExecutionPlan`, `ExecutionResult`.
- **Value Objects:** Strongly typed constructs like `ExecutionId`, `InstructionId`.
- **Exceptions:** Base `PlatformMindException` and domain-specific errors.

### `src/platformmind/infrastructure`
The implementation layer for all external concerns.
- **Database (`infrastructure/database/`):** SQLAlchemy ORM models and repository implementations (SQLite).
- **GitHub (`infrastructure/github/`):** The `GitHubClient` and specific tool implementations.
- **LLM (`infrastructure/llm/`):** LLM Provider implementations (e.g., GroqProvider).
- **Logging (`infrastructure/logging/`):** Application-wide structured logging.

### `src/platformmind/core`
Cross-cutting utilities including application settings loaded via `pydantic-settings` (`config/settings.py`) and standard library wrappers (e.g., `clock.py`).

## Configuration Files
- **`pyproject.toml`**: Defines project dependencies, managed by `uv`.
- **`.env`**: Local environment variables containing secrets like `GITHUB_TOKEN` and `GROQ_API_KEY`.

## Tests
The `tests/` directory strictly mirrors the separation of concerns. Unit tests isolate domain and application logic using mocks (`tests/mocks/`), while integration tests validate infrastructure adapters against real or simulated external systems.

## Related Documents
- [System Architecture](architecture/SYSTEM_ARCHITECTURE.md)
- [Clean Architecture](architecture/CLEAN_ARCHITECTURE.md)
- [Getting Started](development/GETTING_STARTED.md)
