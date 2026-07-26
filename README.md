# PlatformMind 🧠

> An autonomous, self-learning GitHub operations agent built with Python and FastAPI.

🔥 **Live Demo (Swagger UI)**: [https://platformmind.onrender.com/docs](https://platformmind.onrender.com/docs)
🌐 **Production API**: `https://platformmind.onrender.com`

PlatformMind is a production-grade AI agent designed to autonomously manage GitHub repositories by interpreting natural language instructions, breaking them down into dependency-mapped plans, and executing them flawlessly. 

It features a built-in memory system that allows it to learn from past executions and synthesize new capabilities on the fly.

---

## 🌟 Key Features

* **Advanced Planner**: Decomposes natural language requests into topological dependency graphs without relying on hardcoded workflows.
* **LLM Abstraction Engine**: Natively supports multiple LLMs including **Groq**, **Gemini**, and **Ollama** via a unified `LLMProvider` interface.
* **Execution Engine**: Sandboxes and runs complex, multi-step workflows.
* **Learning & Capability Synthesis**: If a workflow is missing, the Synthesis Engine writes it, tests it in a sandbox, and persists it to Memory for future reuse.
* **Enterprise Observability**: Deeply instrumented with OpenTelemetry (OTLP) and natively integrated with **Langfuse** for complete LLM trace visibility.
* **Clean Architecture**: Adheres strictly to Domain-Driven Design (DDD) to decouple business logic from infrastructure.

## 🚀 Deployment

PlatformMind is fully dockerized and ready for production deployment.

### Current Production Stack
* **Web Service**: Hosted on **Render** using Docker.
* **Database**: Serverless PostgreSQL hosted on **Supabase** (powered by asynchronous `asyncpg`).
* **Observability**: **Langfuse** cloud and/or a self-hosted **Jaeger** instance on **Fly.io**.

## 📖 Documentation

Comprehensive, engineer-focused documentation is available in the `docs/` directory.

* 🗺️ [Project Map](docs/PROJECT_MAP.md) - Understand the repository structure.
* 🏛️ [System Architecture](docs/architecture/SYSTEM_ARCHITECTURE.md) - High-level overview of the entire system.
* 🚦 [API Reference](docs/api/API_REFERENCE.md) - Endpoints and workflows.
* 🛠️ [Getting Started](docs/development/GETTING_STARTED.md) - Local development setup.

To get started reading the internal docs, head over to the [Docs README](docs/README.md).

## 🔭 Observability & Tracing

PlatformMind uses Langfuse to monitor the execution engine's LLM calls, latency, tokens, and cost. 

To enable tracing locally:
1. Add your Langfuse keys to `.env` (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`).
2. Boot the API. The `llm_tracer` will automatically detect your keys and trace all Groq/Gemini calls!

*(If you prefer Jaeger, you can route the OpenTelemetry OTLP endpoint to a local Jaeger container).*

## 🧪 Testing

The repository maintains full coverage through `pytest`. 
```bash
uv run pytest
```
*Note: All Git history commits were reconstructed using rigorous CI guardrails requiring `ruff`, `mypy`, and `pytest` to pass sequentially.*
