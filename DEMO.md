# PlatformMind Demo Instructions

The following three instructions will be run live during the walkthrough to demonstrate the core capabilities of PlatformMind, including task decomposition, capability synthesis, and the self-learning loop.

## Instruction 1: Basic Decomposition and Execution
**Instruction:** "Create a high-priority bug report for the login timeout issue and assign it the bug label."

**Expected Agent Behavior:**
1. The planner decomposes the instruction into two steps: `create_issue` and `assign_label`.
2. The agent executes `create_issue` first.
3. The agent passes the newly generated Issue ID to the `assign_label` tool.
4. The execution memory logs the API duration and the new issue ID.

## Instruction 2: Capability Synthesis at Runtime
**Instruction:** "Find all open issues assigned to nobody, group them by priority, and create a weekly triage summary issue."

**Expected Agent Behavior:**
1. The planner attempts to decompose the instruction but detects a capability gap (it doesn't have a native tool to group and format a summary).
2. The `CapabilitySynthesisEngine` invokes the LLM to dynamically generate a new composite workflow.
3. The `SandboxTester` uses static LLM analysis to verify the synthesized plan is safe to execute.
4. The new capability is registered and the agent successfully executes the summary generation.

## Instruction 3: Self-Learning Loop via Knowledge Caching
**Instruction:** "Find the login timeout bug and close it."

**Expected Agent Behavior:**
1. **Run 1:** The agent executes a `search_issues` API call to find the ID of the "login timeout bug", and then calls `close_issue`. (Takes 2 API calls).
2. **Run 2 (Repeated Instruction):** The `PlanOptimizer` interrogates the Execution Memory. It identifies that it previously successfully located this exact bug. 
3. **Behavior Change:** The agent prunes the `search_issues` step from the plan and injects the cached Issue ID directly into the `close_issue` tool.
4. **Measurable Result:** The execution succeeds in 1 API call instead of 2, demonstrating a clear drop in latency and API footprint.