---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/application/planner/pipeline.py`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Capability Synthesis Example

## Purpose
Illustrates what happens when PlatformMind is asked to do something it doesn't know.

## Scenario
**User Instruction:** "Create a milestone called 'Q3 Goals' and attach issue #12 and #14 to it."

### 1. Intent Classification
The planner determines it needs to:
- Create Milestone
- Update Issue #12
- Update Issue #14

### 2. Memory Retrieval Miss
The `MemoryEngine` returns no `Capabilities` that match this exact sequence.

### 3. Synthesis Phase
The `TaskDecomposer` prompts the LLM:
*"I have tools `CreateMilestoneTool` and `UpdateIssueTool`. Create a DAG."*

The LLM generates:
```json
{
  "steps": [
    {"id": "s1", "tool": "create_milestone", "inputs": {"title": "Q3 Goals"}},
    {"id": "s2", "tool": "update_issue", "inputs": {"issue_number": 12, "milestone": "$s1.milestone_id"}},
    {"id": "s3", "tool": "update_issue", "inputs": {"issue_number": 14, "milestone": "$s1.milestone_id"}}
  ]
}
```

### 4. Sandbox Execution
The DAG is executed. It works. 

### 5. Memory Commitment
The `LearningEngine` hashes the DAG structure and stores it in `ChromaDB` as a new Capability. Next time a similar request is made, step 3 is skipped entirely.
