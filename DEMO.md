# PlatformMind Demonstration Guide

This guide outlines a 15-minute video walkthrough to demonstrate that PlatformMind satisfies all assignment requirements.

## 1. Project Overview & Architecture (3 mins)
- Open `FINAL_REPORT.md` and show the Mermaid Architecture Diagram.
- Highlight the 6 Core Engines: Planner, Execution, Memory, Learning, Synthesis, Reporting.
- Show the directory structure to prove adherence to Clean Architecture (no business logic in `api/`).

## 2. Live Demo 1: Simple Task & Execution (3 mins)
**Instruction:** "Create a GitHub issue titled 'Login timeout bug' with labels 'bug' and 'high-priority'."

**Action:**
Send a `POST` request to `/api/v1/execute`:
```json
{
  "instruction": "Create a GitHub issue titled 'Login timeout bug' with labels 'bug' and 'high-priority'.",
  "repository": "my-org/my-repo"
}
```
**Talking Points:**
- Show the API returning the `execution_id`.
- Hit the `/api/v1/reports` endpoint and fetch the execution report.
- Point out the Planner's `Dependency Graph` and the Execution Engine's tool success.

## 3. Live Demo 2: Compound Workflow (3 mins)
**Instruction:** "Find all open issues without an assignee. Group them by label. Create a new issue summarizing the findings."

**Action:**
Send the instruction to `/api/v1/execute`.

**Talking Points:**
- Show the Execution Report. Highlight the `Timeline` array demonstrating task decomposition: `search_issues` -> `create_issue`.
- Emphasize how the Planner decomposed the natural language into sequential, dependency-ordered steps without hardcoded lookup tables.

## 4. Live Demo 3: Capability Synthesis (4 mins)
**Instruction:** "Review all open issues. Generate a markdown release summary. Create a GitHub issue containing the release summary."

**Action:**
Send the instruction to `/api/v1/execute`.

**Talking Points:**
- **Run 1:** Point out in the logs that the Planner failed to find an existing workflow. Show the `Capability Synthesis Engine` spinning up, reasoning about the gap, sandboxing the new workflow, and registering it to Memory.
- **Run 2:** Execute the *exact same instruction* again.
- Show the Execution Report: Highlight `capability_reused: true`. Prove that the system did not re-synthesize but instead fetched the new workflow from Capability Memory.

## 5. Learning Improvements & Final Polish (2 mins)
- Hit the `/api/v1/metrics` endpoint.
- Show the JSON payload indicating `time_improvement_pct` and `retries_improvement_pct`.
- Explain how the `Learning Engine` uses EMA to adjust tool confidence scores over time.
- Open `COMPLIANCE_MATRIX.md` to show that every requirement has been met.

---
*End of Demo.*