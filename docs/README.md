---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind`, `tests`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# PlatformMind Documentation

Welcome to the PlatformMind documentation. PlatformMind is a production-grade, self-learning autonomous GitHub operations agent built with Python and FastAPI. This documentation system is organized to help engineers understand, build, run, debug, extend, and maintain the system.

## Purpose
This documentation serves as the single source of truth for the PlatformMind architecture, internal APIs, and workflows. It is strictly derived from the current repository implementation.

## Folder Structure

The documentation is organized logically into the following directories:

| Directory | Purpose |
| --- | --- |
| `architecture/` | Core architectural components, data flow, and layers (Clean Architecture, DDD). |
| `diagrams/` | Mermaid sequence, state, and component diagrams mapping the implementation. |
| `api/` | FastAPI REST endpoint documentation, models, and execution flows. |
| `development/` | Setup, testing, coding standards, deployment, and contribution workflows. |
| `features/` | Deep dives into core subsystems (Planner, Execution Engine, Memory, Learning). |
| `examples/` | Real application execution outputs, memory transitions, and planner decomposition. |
| `adr/` | Architecture Decision Records explaining *why* key technical choices were made. |
| `troubleshooting/` | Developer guides for debugging, diagnosing errors, and maintaining the system. |

## Reading Order

For new developers joining the project, we recommend the following reading order:

1. [Project Map](PROJECT_MAP.md) - Understand the repository structure and entry points.
2. [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) - High-level overview of the entire system.
3. [Getting Started](development/GETTING_STARTED.md) - Setup and run the application locally.
4. [Clean Architecture ADR](adr/ADR-001-clean-architecture.md) - Understand the architectural constraints.
5. [Planner Pipeline](features/PLANNER.md) - Learn how natural language becomes an execution plan.

## Quick Links

- [API Reference](api/API_REFERENCE.md)
- [Execution Engine](features/EXECUTION_LIFECYCLE.md)
- [Memory Retrieval Flow](features/MEMORY_RETRIEVAL.md)
- [Capability Synthesis](features/RUNTIME_SYNTHESIS.md)
- [Testing Guide](development/TESTING_GUIDE.md)

## Mermaid Diagram Index

Visualizing the system is crucial. Key diagrams include:
- [Overall System Flow](diagrams/overall-system.md)
- [Request Lifecycle](diagrams/request-lifecycle.md)
- [Execution Pipeline Sequence](diagrams/sequence-execute.md)
- [Memory Retrieval Flow](diagrams/memory-retrieval.md)
- [Learning Loop](diagrams/learning-loop.md)
