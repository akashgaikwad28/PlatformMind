---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/application/memory/components/ranker.py`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Memory Retrieval

## Purpose
Details the exact mechanism for finding similar past experiences.

## Responsibilities
Extracting the most semantically relevant memories and ranking them for prompt injection.

## Location in Codebase
- `src/platformmind/application/memory/components/ranker.py`
- `src/platformmind/application/memory/components/compactor.py`

## Related Modules
- [Memory System](MEMORY_SYSTEM.md)

## Dependencies
VectorStore (ChromaDB), Sentence-transformers.

## Internal Workflow
1. The `Instruction` is vectorized.
2. Cosine similarity search retrieves the top K records from ChromaDB.
3. `MemoryRanker` applies a weighted score combining:
   - Semantic similarity score.
   - Recency (time decay).
   - Historical success rate (for capabilities).
4. `MemoryCompactor` truncates the ranked list to fit within the configured token budget.

## Input
`Instruction` vector, raw memory records.

## Output
Ranked and compacted `MemoryContext`.

## Error Handling
N/A

## Performance Notes
Embedding generation takes ~50ms locally. Retrieval takes ~5ms.

## Extension Points
The ranking algorithm can be customized by extending `MemoryRanker`.

## Current Limitations
- Pure semantic search struggles with keyword-specific matches (e.g. searching for a specific PR number).

## Future Improvements
- Implement Hybrid Search (BM25 + Dense Vectors) for better exact-match retrieval.
