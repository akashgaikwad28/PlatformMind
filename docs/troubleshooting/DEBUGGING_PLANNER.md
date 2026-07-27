---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/application/planner/`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Debugging the Planner

## Purpose
Guide to fixing issues when the Planner generates the wrong ExecutionPlan.

## Common Symptoms
The agent attempts to execute the wrong tool, or fails to find a tool.

## Tool Not Found
**Symptom:** API returns `UnsupportedInstructionError` without synthesizing.
**Resolution:** Check `ToolRegistry`. The tool might be registered but its `description` string is too ambiguous for the semantic search to match it to the user's intent. Expand the docstring in the tool class.

## Malformed DAG Dependencies
**Symptom:** Execution engine crashes because a step relies on a variable that hasn't been returned by a previous step.
**Resolution:** This is an LLM hallucination in the `TaskDecomposer`. The prompt must be tuned. Check `src/platformmind/application/planner/prompts.py` and ensure the few-shot examples clearly demonstrate how to link output variables to inputs.

## High Latency
**Symptom:** API takes >5 seconds to return.
**Resolution:** Capability Synthesis might be triggering. Set `LOG_LEVEL=DEBUG` and check if the agent is stuck in the synthesis loop. If so, manually seed the capability or improve the tool descriptions.
