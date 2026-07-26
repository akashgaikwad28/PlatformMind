---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/api/container.py`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# ADR-004: Choice of ChromaDB

## Purpose
This document records the decision to use ChromaDB as the primary vector database for Semantic Memory.

## Responsibilities
ChromaDB handles the storage, indexing, and retrieval of embedded instructions and execution summaries.

## Location in Codebase
- VectorDB implementation injected via `src/platformmind/api/container.py`.

## Related Modules
- [Memory System](../features/MEMORY_SYSTEM.md)
- [System Architecture](../architecture/SYSTEM_ARCHITECTURE.md)

## Dependencies
ChromaDB client library.

## Internal Workflow
Text is vectorized (currently via sentence-transformers) and stored in collections. On retrieval, similar vectors are fetched using cosine similarity.

## Input
Raw text and metadata.

## Output
Top-K similar records.

## Error Handling
Exceptions are caught at the infrastructure boundary and mapped to empty memory results.

## Performance Notes
ChromaDB operates embedded locally, meaning network overhead is eliminated, providing sub-millisecond retrieval.

## Extension Points
The interface allows swapping to a remote vector database (e.g., Pinecone or Qdrant) if scaling is required.

## Current Limitations
- Scalability is bounded by the host machine's memory and disk.

## Future Improvements
- Evaluate migrating to a managed vector store if concurrent multi-tenant loads increase.
