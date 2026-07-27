# PlatformMind

An autonomous, self-learning platform intelligence agent for GitHub operations, built with Python and FastAPI.

**Live Demo (Swagger UI)**: [https://platformmind.onrender.com/docs](https://platformmind.onrender.com/docs)  
**Production API**: `https://platformmind.onrender.com`

## Overview

PlatformMind is a production-grade AI agent designed to autonomously manage GitHub repositories by interpreting natural language instructions, decomposing them into executable workflows, and natively interacting with the GitHub API. 

Unlike traditional automation frameworks that rely on static macros or predefined integrations, PlatformMind features a dynamically self-improving cognitive architecture. It leverages a persistent memory system to learn from past executions, actively reduces its API footprint over time via knowledge caching, and synthesizes entirely new execution capabilities at runtime when encountering novel tasks.

## Key Features

- **Advanced Execution Planner**: Decomposes natural language requests into topological dependency graphs, executing complex tasks through dynamic ReAct loops without relying on hardcoded scripts.
- **Genuine Capability Synthesis**: If a required GitHub operation is missing natively, the Synthesis Engine dynamically reasons about the gap, generates a composite API workflow via static LLM analysis, validates it in a sandbox, and persists it for future reuse.
- **Persistent Memory Engine**: Segregates knowledge into distinct layers (Execution Memory, Capability Memory, Constraint Memory). It utilizes this data to drive behavior, providing few-shot examples for intent classification and biasing tool selection based on historical success rates.
- **Self-Learning Loop (Knowledge Caching)**: Actively measures performance and identifies recurring tasks. By querying historical execution traces, it prunes redundant API lookups (e.g., searching for issue IDs) and injects cached context into subsequent steps, measurably dropping latency and execution cost on run N vs run 1.
- **Enterprise Observability**: Deeply instrumented telemetry via Langfuse for complete LLM trace visibility, cost tracking, and execution performance metrics.
- **Clean Architecture**: Adheres strictly to Domain-Driven Design (DDD), decoupling business logic from infrastructure and allowing seamless dependency injection.

## Technology Stack

- **Core Application**: Python 3.13, FastAPI, Pydantic, AnyIO
- **Database / Persistence**: SQLAlchemy 2.0 (Async), SQLite (Local) / PostgreSQL (Production)
- **Intelligence / LLM Engine**: Groq (Llama-3.3-70b-versatile), unified `LLMProvider` interface
- **Observability**: Langfuse (OpenTelemetry compatible traces)
- **Dependency Management**: `uv` package manager
- **Code Quality**: Ruff (Linting/Formatting), MyPy (Type Checking), Pytest (Unit/E2E Testing)

## Local Development and Execution

PlatformMind is designed to run seamlessly in local environments utilizing the `uv` package manager.

### Prerequisites

- Python 3.13+
- `uv` installed on your system
- A GitHub Personal Access Token (Classic or Fine-grained)
- A Groq API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/akashgaikwad28/PlatformMind.git
   cd PlatformMind
   ```

2. **Configure Environment Variables:**
   Copy the example environment file and provide your credentials.
   ```bash
   cp .env.example .env
   ```
   Open `.env` and configure at minimum:
   ```env
   GROQ_API_KEY="your_groq_api_key"
   GITHUB_TOKEN="your_github_token"
   GITHUB_OWNER="your_github_username"
   GITHUB_REPOSITORY="your_github_username/PlatformMind"
   DATABASE_URL="sqlite+aiosqlite:///./data/platformmind.db"
   ```

3. **Install Dependencies:**
   ```bash
   uv sync
   ```

### Running the Application

Start the FastAPI application using the built-in development server:

```bash
uv run fastapi dev src/platformmind/api/app.py
```
Alternatively, to run in production mode:
```bash
uv run fastapi run src/platformmind/api/app.py
```

The API will be available at `http://127.0.0.1:8000`. You can interact with the agent via the Swagger UI available at `http://127.0.0.1:8000/docs`.

### Testing

The repository maintains rigorous coverage through `pytest`. To execute the test suite:
```bash
uv run pytest
```

## System Architecture and Documentation

Comprehensive engineering documentation is available in the `docs/` directory or at the root of the repository.

- [ARCHITECTURE.md](ARCHITECTURE.md) - Summary of the Memory, Synthesis, and Learning implementations.
- [DEMO.md](DEMO.md) - Sample instructions of increasing complexity for executing the agent.
- [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md) - Detailed guide for validating the API and system capabilities.
- [DIAGRAM_MEMORY_FLOW.md](DIAGRAM_MEMORY_FLOW.md) - Visual mapping of the Execution and Capability memory structures.
- [DIAGRAM_CAPABILITY_SYNTHESIS.md](DIAGRAM_CAPABILITY_SYNTHESIS.md) - Walkthrough of runtime capability generation and sandboxing.
- [DIAGRAM_LEARNING_LOOP.md](DIAGRAM_LEARNING_LOOP.md) - Demonstration of the self-learning feedback and caching cycle.
