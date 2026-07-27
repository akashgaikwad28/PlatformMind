# ARCHITECTURE

# PlatformMind – Autonomous Platform Intelligence Agent

## Platform

**GitHub**

PlatformMind is an autonomous GitHub agent that converts natural language instructions into executable workflows. It plans tasks, executes real GitHub API operations, learns from every execution, and synthesizes new reusable capabilities when it encounters previously unknown tasks.

---

# 1. What does the memory system store, and why is it structured this way?

The memory system is designed to store **structured operational knowledge**, not chat history or prompt logs.

It consists of four complementary layers:

### Execution Memory
Stores previous executions including:

- Original instruction
- Generated execution plan
- Executed steps
- Success/failure status
- API calls
- Execution time
- Retry count
- Errors encountered
- Constraints discovered

This allows the agent to reuse successful execution strategies and avoid previously failed approaches.

### Capability Memory

Stores reusable capabilities the agent knows how to perform.

Each capability contains:

- Capability name
- Required inputs
- Execution strategy
- Tool sequence
- Success rate
- Average execution cost
- Average execution time

The planner consults this memory before generating a new workflow so existing capabilities are reused instead of recreated.

### Semantic Memory

Instructions and execution summaries are embedded using sentence embeddings and stored in ChromaDB.

Before planning, similar historical executions are retrieved using semantic similarity.

This enables the planner to leverage experience from related tasks rather than relying solely on the LLM.

### Learning Memory

Stores long-term performance metrics including:

- Success rate
- Failure rate
- Retry statistics
- Tool effectiveness
- Platform constraints
- Best execution strategies

The learning engine continuously updates these metrics after every execution.

---

# 2. How does capability synthesis work?

When the planner encounters an instruction that cannot be solved using existing capabilities, it enters the capability synthesis pipeline.

The pipeline performs the following steps:

1. Detect the capability gap.
2. Reason about the missing operation.
3. Generate a candidate workflow by composing existing tools or generating a new execution strategy.
4. Validate the generated workflow.
5. Execute the workflow in a controlled manner.
6. If successful, register it as a new capability.
7. Persist the capability in Capability Memory for future reuse.

Future executions reuse the synthesized capability directly instead of generating it again.

This allows the system to expand its abilities at runtime without manually implementing every possible workflow.

---

# 3. What is the learning signal, and what changes on run N compared to run 1?

The primary learning signal is **execution performance**.

After every execution the agent records:

- Execution duration
- Number of API calls
- Retry count
- Success or failure
- Constraints discovered
- Tool effectiveness

These metrics directly influence future planning.

Examples of behavioral improvements include:

- Selecting tools with higher historical success rates.
- Avoiding workflows that previously failed.
- Remembering repository-specific constraints.
- Reusing synthesized capabilities instead of rebuilding them.
- Retrieving similar successful executions before planning.

### Example

**Run 1**

Instruction:

> Copy labels from Repository A to Repository B.

The capability does not exist.

The agent synthesizes a workflow using existing GitHub operations, validates it, executes it, and stores the resulting capability.

- Planning time: 2.8 seconds
- API calls: 9

**Run 5**

The same instruction is received.

The planner retrieves the existing synthesized capability from Capability Memory instead of generating a new workflow.

- Planning time: 0.5 seconds
- API calls: 5

The measurable improvement demonstrates that PlatformMind learns from experience and changes its behavior over time.

---

PlatformMind follows Clean Architecture, Domain-Driven Design (DDD), and Hexagonal Architecture to ensure business logic remains independent from infrastructure, making the system modular, maintainable, and easily extensible to additional SaaS platforms beyond GitHub.