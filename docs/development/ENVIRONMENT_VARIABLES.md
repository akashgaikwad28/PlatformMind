---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/core/config/`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Environment Variables

## Purpose
Defines the required and optional configurations for the application.

## Location in Codebase
- `src/platformmind/core/config/settings.py`
- `.env.example`

## Required Variables
| Variable | Description | Example |
| --- | --- | --- |
| `GROQ_API_KEY` | Key for LLM Inference | `gsk_abc...` |
| `GITHUB_TOKEN` | PAT for GitHub Operations | `ghp_123...` |

## Optional Variables
| Variable | Default | Description |
| --- | --- | --- |
| `LOG_LEVEL` | `INFO` | Output verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `DATABASE_URL` | `sqlite+aiosqlite:///platformmind.db` | Connection string for structured memory |
| `CHROMA_DB_PATH` | `./chroma_db` | Path for vector persistence |

## Loading Mechanism
Pydantic `BaseSettings` handles loading from the `.env` file and environment injection. It performs type coercion and validation at startup. If required variables are missing, the application halts immediately.
