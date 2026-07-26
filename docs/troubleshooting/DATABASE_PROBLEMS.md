---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/infrastructure/database/`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Troubleshooting Database Problems

## Purpose
Resolve issues with SQLite or ChromaDB.

## Common Symptoms
Memory retrieval fails or executions are not saved.

## SQLite Database Locked
```
sqlite3.OperationalError: database is locked
```
**Cause:** High concurrency writes. SQLite only supports a single writer.
**Resolution:** Reduce parallel request load or migrate to PostgreSQL.

## ChromaDB Directory Lock
```
chromadb.errors.InvalidCollectionException
```
**Cause:** ChromaDB state mismatch, often caused by abruptly killing the server during a write.
**Resolution:** Delete the `./chroma_db` directory to force a fresh index. (Note: Semantic history will be lost).

## Alembic Migration Conflicts
```
Target database is not up to date.
```
**Cause:** The schema in code does not match the schema in SQLite.
**Resolution:** Run `uv run alembic upgrade head`. If local dev data is disposable, delete `platformmind.db` and let it auto-create.
