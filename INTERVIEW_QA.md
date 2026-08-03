# 50 AI Engineer Interview Q&A — PlatformMind

---

## Section 1: System Architecture & Design

**Q1. What is PlatformMind and what problem does it solve?**
> PlatformMind is an autonomous GitHub management agent. It takes natural-language instructions (e.g., "create a bug issue and assign it to the backlog milestone"), plans a multi-step execution sequence, runs those steps via GitHub's API, learns from every execution, and improves over time — removing the need for manual GitHub project management.

---

**Q2. What architectural pattern does PlatformMind follow?**
> Clean Architecture with Domain-Driven Design. The code is split into four concentric layers:
> - **Domain** — pure business models and interfaces (no external dependencies)
> - **Application** — use-case orchestrators, engines, and services
> - **Infrastructure** — concrete implementations (DB, GitHub client, ChromaDB, LLM)
> - **API** — FastAPI routers, middleware, and dependency injection container

This ensures the core logic is completely decoupled from any specific framework or database.

---

**Q3. Why is Clean Architecture beneficial for an AI agent?**
> AI agents are highly experimental — you frequently swap LLM providers, vector databases, or external APIs. Clean Architecture lets you swap any infrastructure component (e.g., replace ChromaDB with Qdrant, or Groq with OpenAI) without touching business logic, because only the interface matters, not the concrete implementation.

---

**Q4. Explain the dependency injection pattern used in the project.**
> FastAPI's built-in dependency injection system is used. The `container.py` wires up all concrete implementations at startup and stores references on the `app.state`. The `dependencies.py` file provides typed `get_*` functions (e.g., `get_execution_engine`) that the routers consume. This makes testing easy — you override dependencies with mock implementations via `app.dependency_overrides`.

---

**Q5. What is the role of the `ExecutionOrchestrator`?**
> It is the central coordinator for executing a plan. It iterates over topologically-sorted plan steps, resolves inter-step references (e.g., `@step_1.issue_number`), calls the `StepExecutor` with retry logic, tracks metrics, and if a step fails permanently, triggers the `RollbackManager` to undo all previously completed steps.

---

## Section 2: Agentic AI & LLMs

**Q6. What is the ReAct (Reason + Act) loop in PlatformMind?**
> The `PlatformMindAppService.execute()` method implements a ReAct loop with up to 5 iterations. In each cycle: (1) the Planner reasons about the instruction and generates a plan, (2) the Orchestrator acts by executing the plan's tools, (3) the results are fed back as `previous_results` for the next planning cycle. This allows dynamic replanning if early steps return unexpected results.

---

**Q7. How does the Planner work end-to-end?**
> The `PlanningPipeline` runs these stages in order:
> 1. Normalize the instruction text
> 2. Build planning context from memory
> 3. Classify the user's intent (via LLM)
> 4. Decompose into sub-tasks (via LLM)
> 5. Match capabilities / select tools
> 6. Resolve inter-step dependencies
> 7. Optimize and validate the plan
> 8. Apply input guardrails

The final output is a typed `ExecutionPlan` with ordered `ExecutionStep` objects.

---

**Q8. How does the system handle LLM hallucinations in planning?**
> Several safeguards exist: (1) Input guardrails reject ambiguous or dangerous instructions, (2) the `ExecutionPlanValidator` checks that every tool referenced actually exists in the registry, (3) `_resolve_inputs` in the Orchestrator catches placeholder values like `{{issue_number}}` and resolves them from prior step outputs, and (4) the retry manager retries transient failures.

---

**Q9. What is Capability Synthesis?**
> When the Planner identifies a capability gap — an instruction that cannot be fulfilled by existing native tools — the `CapabilitySynthesisEngine` reasons about the gap using an LLM, designs a new workflow definition, validates it in a sandbox, and registers it. Future instructions can then reuse this synthesized capability.

---

**Q10. What is the role of the Intent Classifier?**
> The `IntentClassifier` uses an LLM call to map raw user text to a structured intent category (e.g., `CREATE_ISSUE`, `MANAGE_LABELS`, `SEARCH_ISSUES`). This intent is then used by the `TaskDecomposer` and `ToolSelector` to generate the appropriate execution plan, rather than passing the raw text directly to each component.

---

## Section 3: Memory & Learning

**Q11. Describe the four types of memory in PlatformMind.**
> 1. **Execution Memory** — stores past execution records (instruction, result, metrics) in the relational DB and semantically indexes them in ChromaDB.
> 2. **Capability Memory** — tracks all available tools (native and synthesized) and their performance stats.
> 3. **Constraint Memory** — stores learned rules (e.g., "GitHub API labels must not have a leading `#` in color codes").
> 4. **Learning Memory** — tracks improvement metrics, trends, and planner strategy evolution.

---

**Q12. How does semantic memory retrieval work?**
> When the Planner needs context, the `MemoryRetriever` calls `ExecutionMemoryService.find_similar_executions(query)`. This embeds the query using the LLM's embedding API, then performs a cosine-similarity search in ChromaDB. The top-N most semantically similar past executions are returned and injected into the planning context.

---

**Q13. Why was ChromaDB chosen over a simple in-memory dict for vector storage?**
> The original `VectorDBImpl` was a naive in-memory cosine-similarity dict. It had two problems: (1) it was lost on every server restart, and (2) it scaled `O(n)` with the number of stored vectors. ChromaDB provides persistent on-disk storage, HNSW-based approximate nearest-neighbor indexing (`O(log n)` search), and a production-ready Python client, making it far more robust.

---

**Q14. How does the Learning Engine improve the agent over time?**
> The `LearningEngineImpl` runs after every execution: the `ExecutionAnalyzer` extracts constraints and patterns, the `MetricsCollector` records performance data, the `ImprovementCalculator` computes deltas from prior runs, and the `TrendAnalyzer` detects if performance is improving or degrading. Results are persisted so future planning cycles benefit from the accumulated knowledge.

---

**Q15. What is memory compaction and why is it needed?**
> Over time the execution history grows very large. `MemoryCompactor` runs periodically to summarize and archive old records using the LLM (the `MemorySummarizer`). This keeps the active memory manageable and prevents context windows from being overwhelmed with stale, low-value data.

---

## Section 4: Execution, Tools & Rollbacks

**Q16. How are tools registered and discovered?**
> The `ToolRegistry` is a simple dict-based registry (`{name: BaseTool}`). At startup, `container.py` instantiates each concrete tool (e.g., `CreateIssueTool`, `AssignLabelTool`) with a shared `GitHubClient` and registers it. The Planner's `ToolSelector` references this registry to know which tools are available when building plans.

---

**Q17. Explain the `BaseTool` contract.**
> Every tool inherits `BaseTool[TInput]`. The `run(**kwargs)` method: (1) validates kwargs against a Pydantic `input_schema`, (2) calls the abstract `_execute(validated_input)` method, (3) wraps the result in a standardized `ToolResult`. Subclasses implement `_execute` and can optionally return a 4-tuple including a `compensation` async callback for rollback purposes.

---

**Q18. What is the rollback system and how does it work?**
> It is a Saga-pattern rollback mechanism. When a tool succeeds, if it returns a `compensation` callable, the `ExecutionOrchestrator` registers it with `RollbackManager`. If a subsequent step fails permanently, `RollbackManager.rollback()` is called, which executes all registered compensations in **reverse order**. For example: if Step 1 created an issue and Step 2 failed, the compensation for Step 1 closes the created issue, leaving the repository in a clean state.

---

**Q19. Give a specific example of a rollback compensation.**
> `CreateIssueTool._execute()` returns a closure `compensate()` that calls `PATCH /repos/{owner}/{repo}/issues/{number}` with `{"state": "closed"}`. This is the inverse of creation. Similarly, `AssignLabelTool` returns a compensation that deletes each label it added by calling `DELETE /repos/{owner}/{repo}/issues/{number}/labels/{label}`.

---

**Q20. What is the Retry Manager?**
> `RetryManager` wraps any async action with configurable retry logic. It retries up to `max_retries` times with exponential backoff (`base_delay * 2^attempt`). A pluggable `is_retryable` predicate function determines whether a given exception should trigger a retry (e.g., 429 rate-limit errors should retry; validation errors should not).

---

## Section 5: Infrastructure & Database

**Q21. What database does PlatformMind use and why async?**
> SQLAlchemy 2.0 with `create_async_engine`. In production it connects to PostgreSQL via the `asyncpg` driver; locally it uses SQLite via `aiosqlite`. Async I/O is critical in a FastAPI application — blocking DB calls on the async event loop would stall all concurrent requests.

---

**Q22. What is the Unit of Work pattern?**
> `UnitOfWork` wraps a SQLAlchemy `AsyncSession` in an async context manager. It provides atomic transactional boundaries: on `__aenter__` it opens the session, on `__aexit__` with no exception it commits, on exception it rolls back. This ensures that partial writes are never persisted to the database.

---

**Q23. How are database migrations handled?**
> Alembic is configured (`alembic.ini` and `alembic/` directory) for schema migrations. Developers create versioned migration scripts that can be applied (`alembic upgrade head`) or reversed (`alembic downgrade -1`), enabling safe, reproducible schema evolution across environments.

---

**Q24. What is the Repository pattern and why use it here?**
> Each domain aggregate has an abstract `Repository` interface (e.g., `ExecutionRepository`) with CRUD methods. Concrete implementations (`ExecutionRepositoryImpl`) use SQLAlchemy to fulfill the contract. This means application-layer services depend only on the abstract interface, not on SQLAlchemy directly — making them unit-testable without a real database.

---

**Q25. How does the `ChromaVectorStore` integrate with the async event loop?**
> ChromaDB's Python client is synchronous. To avoid blocking the FastAPI event loop, all ChromaDB calls are wrapped in `asyncio.to_thread(...)`, which runs the synchronous function in a thread pool executor. This preserves concurrency without requiring a full async ChromaDB client.

---

## Section 6: API Design & Middleware

**Q26. What API standard does PlatformMind expose?**
> A RESTful API under `/api/v1/` with standard HTTP semantics. Endpoints: `POST /execution` (trigger an instruction), `GET /memory` (view agent memory), `GET /capabilities` (list tools), `GET /metrics` (performance dashboard), `GET /reports` (execution history), `POST /synthesis` (synthesize new capabilities). All responses use typed Pydantic schemas.

---

**Q27. What middleware is applied and what does each do?**
> Three custom middlewares are stacked on FastAPI:
> 1. **`RequestIDMiddleware`** — generates and attaches a unique `X-Request-ID` header for distributed tracing.
> 2. **`TimingMiddleware`** — measures total request duration and adds an `X-Response-Time` header.
> 3. **`LoggingMiddleware`** — logs every request/response with method, path, status, and duration using structured Loguru logging.

---

**Q28. How is observability implemented?**
> Two layers: (1) **Langfuse** is integrated for LLM-specific tracing — it tracks every LLM call (prompt, completion, latency, tokens) and associates them with execution traces. (2) **OpenTelemetry** instrumentation is also wired up for general distributed tracing. The `@trace_step` decorator provides a lightweight span mechanism for key orchestration steps.

---

**Q29. How are exceptions handled globally?**
> Three exception handlers are registered on the FastAPI app: (1) `validation_exception_handler` for Pydantic `RequestValidationError` (returns 422 with field-level detail), (2) `platformmind_exception_handler` for domain-specific `PlatformMindException` subclasses, and (3) `global_exception_handler` as a final catch-all that returns a 500 without leaking stack traces to the client.

---

**Q30. Describe the CI/CD pipeline.**
> GitHub Actions workflows (in `.github/workflows/`) run on every PR: (1) lint with `ruff`, (2) type-check with `mypy`, (3) run `pytest` with coverage report, (4) Docker build validation. A Dockerfile and `docker-compose.yml` are provided for containerized local development and deployment.

---

## Section 7: Testing

**Q31. What testing strategy is used?**
> Three levels: (1) **Unit tests** for pure domain logic and individual components in isolation, (2) **Integration tests** for DB repositories using an in-memory SQLite database, and (3) **API tests** using `httpx.AsyncClient` with ASGI transport and mocked engine dependencies via `app.dependency_overrides`.

---

**Q32. How are tests isolated from the real database?**
> DB integration tests use `sqlite+aiosqlite:///:memory:` — an in-memory SQLite database. The `test_engine` fixture creates all tables via `Base.metadata.create_all` at test start and drops them after. This ensures tests are fully isolated, repeatable, and don't require a running PostgreSQL instance.

---

**Q33. How are external GitHub API calls prevented in tests?**
> The `conftest.py` registers mock classes (`MockExecutionEngine`, `MockMemoryEngine`, etc.) via `app.dependency_overrides`. The API tests never actually hit GitHub. For the sandbox integration test (`test_sandbox.py`), a real `GITHUB_TOKEN` is needed — if absent, it fails with a 404, which is expected and acceptable.

---

**Q34. What is `pytest-asyncio` used for?**
> All application I/O is `async/await`. `pytest-asyncio` provides a `@pytest.mark.asyncio` marker and an async test runner that creates an event loop for each test. With `asyncio_mode = "auto"` set in `pyproject.toml`, all `async def test_*` functions automatically get an event loop without manual decoration.

---

**Q35. What code quality tools are enforced?**
> (1) `ruff` for linting and formatting (replaces flake8 + black), (2) `mypy` in strict mode for static type checking, (3) `pre-commit` hooks that run ruff and mypy before every commit, and (4) `pytest-cov` for code coverage reporting. These are all gated in CI.

---

## Section 8: AI/ML Concepts

**Q36. What is an embedding and how is it used here?**
> An embedding is a dense vector representation of text that captures semantic meaning. When PlatformMind stores an execution, it embeds the instruction+summary into a float vector using the LLM's embedding API. When retrieving similar executions later, the query is also embedded and ChromaDB computes cosine similarity between the query vector and stored vectors to find semantically related results.

---

**Q37. What is cosine similarity and why use it for text embeddings?**
> Cosine similarity measures the angle between two vectors, ranging from -1 (opposite) to 1 (identical). It is preferred for text embeddings because it is magnitude-invariant — a short sentence and a long sentence expressing the same idea will have a high cosine similarity even though their raw vector magnitudes differ. ChromaDB uses `hnsw:space=cosine` for this reason.

---

**Q38. What is HNSW and why does it matter for vector search?**
> HNSW (Hierarchical Navigable Small World) is a graph-based approximate nearest-neighbor (ANN) index. Instead of exhaustively comparing a query vector to every stored vector (O(n)), HNSW navigates a hierarchical graph to find approximate nearest neighbors in O(log n). ChromaDB uses HNSW internally, making similarity search scalable to millions of vectors.

---

**Q39. What is prompt engineering and how is it applied in PlatformMind?**
> Prompt engineering is the practice of crafting LLM input prompts to produce reliably structured outputs. In PlatformMind, the `IntentClassifier` and `TaskDecomposer` use carefully structured prompts that instruct the LLM to respond in specific JSON schemas. This ensures outputs can be deterministically parsed into Pydantic models like `ExecutionPlan`.

---

**Q40. What is temperature in LLM inference and what value would you use here?**
> Temperature controls randomness: 0 = deterministic (always picks the highest-probability token), 1 = very creative/random. For a planning agent where correctness and repeatability are critical, you would use a **low temperature (0.0–0.2)**. For creative tasks like synthesizing a new capability description, a slightly higher temperature (0.4–0.6) could be beneficial.

---

## Section 9: Advanced Concepts & Trade-offs

**Q41. What is the Saga pattern and how does it apply to the rollback system?**
> The Saga pattern manages distributed transactions by decomposing them into a sequence of local transactions, each with a compensating transaction that can undo it. PlatformMind uses a **choreography-style Saga**: each successful tool call registers its own compensation function. If the overall execution fails, compensations run in reverse, ensuring eventual consistency across GitHub API state.

---

**Q42. What trade-off did you make with synchronous ChromaDB calls?**
> ChromaDB's Python client is synchronous. Options were: (1) use `asyncio.to_thread` (chosen) — adds slight overhead per call but is simple and doesn't block the event loop, or (2) use a thread-based executor globally — more efficient but more complex. A future improvement would be adopting the ChromaDB async HTTP client to eliminate thread switching entirely.

---

**Q43. How does the system handle GitHub API rate limits?**
> The `RetryManager` retries failed tool calls with exponential backoff. A 429 (Too Many Requests) response from GitHub triggers a retry with increasing delays. Additionally, the `MemoryRanker` prioritizes cached results from memory so that repeat queries don't always require new API calls, reducing rate limit pressure.

---

**Q44. What is the difference between a capability and a tool in PlatformMind?**
> A **tool** is a concrete GitHub API operation (e.g., `CreateIssueTool`). A **capability** is a higher-level named skill that may map to one or more tools, and tracks performance metadata (usage count, success rate, average execution time). Native tools map 1:1 to capabilities. Synthesized capabilities can be multi-step workflows that the system invents dynamically.

---

**Q45. Why is Pydantic used extensively throughout the codebase?**
> Pydantic provides runtime validation at the boundaries of the system. Every tool validates its inputs via Pydantic `BaseModel`. Every API request/response is validated. Every settings value in `settings.py` is a Pydantic field. This catches data errors early (fail-fast), provides automatic JSON serialization, and generates OpenAPI schema documentation automatically from the models.

---

## Section 10: Behavioral & Design Questions

**Q46. How would you scale PlatformMind to handle hundreds of concurrent users?**
> (1) Deploy multiple FastAPI instances behind a load balancer, (2) switch from per-process in-memory state to a shared Redis cache for session data, (3) move the `ChromaVectorStore` to a dedicated ChromaDB server or Qdrant cluster, (4) use a task queue (e.g., Celery + Redis) for long-running planning+execution flows so HTTP requests don't time out, (5) implement multi-tenant auth so each user's GitHub token is used for their own requests.

---

**Q47. How would you add support for a new GitHub action (e.g., create a pull request)?**
> (1) Create `CreatePRInput(BaseModel)` with the required fields, (2) create `CreatePRTool(BaseTool[CreatePRInput])` implementing `_execute` that calls the GitHub API, with a `compensation` to close the PR, (3) register it in `container.py`'s `ToolRegistry`, (4) add its name and description to the `ToolSelector`'s known tools. No other layer needs to change.

---

**Q48. What would you change about the current architecture?**
> (1) Extract the vector store initialization out of `container.py` and make it lazily initialized, (2) replace the in-process learning loop with an async background task or worker to avoid blocking the main event loop, (3) add a message queue (RabbitMQ/Kafka) between the API and the Executor for reliability and observability, (4) implement proper auth (Phase 4) so the system is truly multi-tenant.

---

**Q49. How is the project structured for maintainability?**
> Each domain concept lives in its own bounded module. Interfaces (ABCs) are defined in `application/interfaces/` and implementations in `infrastructure/`. No circular imports — domain has zero dependencies on application or infrastructure. `pyproject.toml` defines all dependencies, tooling, and test config in one place. Diagrams in `docs/diagrams/` keep architecture documentation in sync with code.

---

**Q50. Explain your biggest technical challenge and how you solved it.**
> **Challenge**: The multi-step execution plan could partially succeed — e.g., an issue gets created but the subsequent label assignment fails. This left the GitHub repository in an inconsistent state with no automated cleanup.

> **Solution**: Implemented a Saga-pattern rollback system. The `ToolResult` schema was extended with an optional `compensation` callable. Each mutating tool (`CreateIssueTool`, `AssignLabelTool`, etc.) returns a closure that performs the inverse operation. The `ExecutionOrchestrator` registers these closures with the `RollbackManager` upon each step's success. On failure, the `RollbackManager` executes them in reverse order, restoring the repository to its pre-execution state — a clean, production-grade solution.
