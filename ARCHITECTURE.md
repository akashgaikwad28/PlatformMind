# PlatformMind Architecture

## 1. What does your memory system store, and why did you structure it that way?
Our memory system leverages a persistent SQLite database (via SQLAlchemy) configured across four distinct layers: Execution Memory, Capability Memory, Constraint Memory, and Learning Memory. 

It stores historical execution traces (original instructions, step decomposition, execution duration, and success status), registered native tools, synthesized capabilities (with rolling success/failure rates), and hard constraints discovered at runtime. 

**Why we structured it this way:** 
A single vector database of past prompts is insufficient for intelligent automation. By segregating memory into distinct domain layers, the agent can actively retrieve different context types for different stages of the planning pipeline. The `Execution Memory` provides few-shot examples for intent classification, while the `Capability Memory` biases the tool selector toward highly successful tools, and `Constraint Memory` feeds into the risk analyzer. This structure ensures memory is actively queried to influence behavior, rather than just logged.

## 2. How does capability synthesis work in your implementation?
Capability synthesis occurs dynamically at runtime when the LLM Planner detects a capability gap (an instruction that cannot be fulfilled by native tools). 

When a gap is detected, the `CapabilitySynthesisEngine` orchestrates a 10-step pipeline. Specifically, the `ReasoningEngine` invokes the LLM (`structured_completion`) to analyze the missing workflow and generate a concrete, step-by-step API call strategy composed of existing atomic operations. This generated workflow is then passed to the `SandboxTester`, which performs a dry-run static analysis (also powered by the LLM) to guarantee safety and validity. If the sandbox validates the workflow, it is dynamically registered in the `CapabilityRegistry`, persisted to Capability Memory, and immediately exposed back to the Planner for subsequent reuse. 

## 3. What is your learning signal, and what does the agent do differently on run N vs run 1?
Our primary learning signal is **API Call Reduction via Knowledge Caching**. 

Every execution is tracked and its traces (inputs, outputs, durations) are saved to Execution Memory. On Run 1 of an instruction (e.g., "Find the login timeout issue and assign it the bug label"), the agent must execute multiple API calls: one to search the repository for the issue ID, and another to apply the label. 

On Run N, the `PlanOptimizer` analyzes the `PlanningContext` prior to execution. If it detects a semantic match in Execution Memory where an entity ID was successfully resolved, it aggressively prunes the redundant search task from the generated DAG and injects the cached Issue ID directly into the mutation step. The agent measurably performs differently: Run 1 takes 2+ API calls and higher latency, whereas Run N skips the search step entirely, executing in 1 API call with dramatically lower latency.