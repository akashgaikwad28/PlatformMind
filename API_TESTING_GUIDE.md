# API Testing Guide

## 1. Purpose of the Document

Welcome to the API Testing Guide for the **PlatformMind** Autonomous Platform Intelligence Agent. This document is intended for recruiters, technical reviewers, and senior software engineers evaluating the project for the Watermelon Software assignment. 

The purpose of this guide is to provide a complete, step-by-step walkthrough to evaluate, validate, and understand the core features of the system without needing prior knowledge of the codebase. By following this guide, reviewers will be able to verify that the project satisfies **every major requirement** of the assignment, including autonomous execution, memory persistence, learning loops, and dynamic capability synthesis.

## 2. Prerequisites

Before running the application or executing these tests, ensure the following prerequisites are met:

- **Python Version**: Python 3.10+ (using `uv` for dependency management).
- **Environment Variables**: Create a `.env` file in the project root with at least the following:
  ```env
  GITHUB_TOKEN=your_classic_github_token
  GROQ_API_KEY=your_groq_api_key
  ENVIRONMENT=development
  ```
- **Required Software**: Git, Python 3.10+, and `uv` package manager.
- **Installation**: Run `uv sync` to install dependencies.
- **Database Initialization**: SQLite is used for local storage, initializing automatically on first run.
- **ChromaDB**: The vector store automatically initializes locally inside the `.chroma` directory.
- **Starting the Server**: Run the following command from the root directory:
  ```bash
  uv run uvicorn platformmind.api.app:create_app --factory --reload --port 8000
  ```

## 3. API Overview

- **Base URL**: `http://127.0.0.1:8000`
- **API Version**: `v1` (routes prefixed with `/api/v1`)
- **Swagger Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **OpenAPI Schema**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)
- **Authentication**: All repository execution requests require a valid `GITHUB_TOKEN` injected via the environment.
- **General Response Format**: Standardized `APIResponse` wrapper.
  ```json
  {
    "status": "success",
    "data": { ... },
    "request_id": "uuid",
    "timestamp": "ISO-8601"
  }
  ```
- **Error Response Format**: Standardized `APIErrorResponse` wrapper.
  ```json
  {
    "status": "error",
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Human readable message",
      "details": []
    },
    "request_id": "uuid",
    "timestamp": "ISO-8601"
  }
  ```

## 4. API Endpoints

### 4.1. `GET /api/health`
- **Purpose**: Validates the health of the API and its underlying engines (Database, External APIs).
- **Expected Behavior**: Returns a 200 OK with system status.
- **Satisfies**: Production-readiness requirements.

### 4.2. `POST /api/v1/execute`
- **Purpose**: Submits a natural language instruction for autonomous execution.
- **Request Format**: 
  ```json
  {
    "instruction": "Create a bug issue",
    "repository": "owner/repo"
  }
  ```
- **Expected Behavior**: Kicks off the Planner -> Orchestrator -> Synthesizer loop and returns a comprehensive `ExecutionReport`.
- **Satisfies**: Core assignment execution loop.

### 4.3. `GET /api/v1/memory`
- **Purpose**: Retrieves current persisted state for capability, constraint, learning, and execution memory.
- **Expected Behavior**: Returns a deeply nested dictionary representing agent memory.
- **Satisfies**: The "Memory Persistence" requirement.

### 4.4. `GET /api/v1/reports`
- **Purpose**: Lists historical execution reports.
- **Expected Behavior**: Returns an array of `ExecutionReportResponse` models.
- **Satisfies**: Structured Reporting requirements.

### 4.5. `GET /api/v1/capabilities`
- **Purpose**: Lists all available native and dynamically synthesized capabilities.
- **Expected Behavior**: Returns a list of capability objects indicating success rates and reuse metrics.
- **Satisfies**: Capability synthesis and management requirements.

### 4.6. `GET /api/v1/metrics`
- **Purpose**: Retrieves learning and system performance metrics.
- **Expected Behavior**: Returns learning metrics like API call reduction and execution speed improvements.
- **Satisfies**: The Learning Loop requirement.

## 5. Complete Testing Workflow

To thoroughly review the agent, follow this exact sequence:

1. **Step 1: Health Check** (`GET /api/health`) - Verify the system is running.
2. **Step 2: Execute Simple Instruction** (`POST /api/v1/execute`) - Trigger a basic repository action.
3. **Step 3: Verify Memory** (`GET /api/v1/memory`) - Ensure the execution and capability usage was logged.
4. **Step 4: Verify Reports** (`GET /api/v1/reports`) - Check the structured markdown/JSON report for the previous run.
5. **Step 5: Verify Metrics** (`GET /api/v1/metrics`) - Check the baseline performance metrics.
6. **Step 6: Execute Similar Instruction Again** (`POST /api/v1/execute`) - Repeat step 2 to trigger learning and caching mechanisms.
7. **Step 7: Verify Learning** (`GET /api/v1/metrics`) - Observe if API calls reduced or execution speed improved.
8. **Step 8: Execute Unknown Instruction** (`POST /api/v1/execute`) - Force the engine into synthesis mode to create a new capability.

## 6. Assignment Demonstration Tests

You can run these via Swagger UI (`http://127.0.0.1:8000/docs`).

### Demo 1: Simple Instruction
- **Example Payload**:
  ```json
  {
    "instruction": "Create a bug issue titled 'Login timeout' with the 'bug' label",
    "repository": "your_github_username/your_test_repo"
  }
  ```
- **Expected**: The LLM parses the intent, selects the native `create_issue` tool, executes it on GitHub, updates memory, and generates a structured report.

### Demo 2: Compound Instruction
- **Example Payload**:
  ```json
  {
    "instruction": "Find all open bug issues and assign them the 'triage' label",
    "repository": "your_github_username/your_test_repo"
  }
  ```
- **Expected**: Task decomposition into two steps: 1) Searching issues, 2) Iterating over results to update labels. The Execution Report will show a multi-step timeline.

### Demo 3: Unknown Instruction Requiring Capability Synthesis
- **Example Payload**:
  ```json
  {
    "instruction": "Perform a bulk audit of repository stargazers and cross-reference them against open PRs",
    "repository": "your_github_username/your_test_repo"
  }
  ```
- **Expected**: The Planner will fail to find native tools for this exact compound workflow. The `CapabilitySynthesisEngine` will intercept, detect the gap, generate a custom python workflow script or chained plan, validate it in the sandbox, register it, and execute it. 

## 7. Memory Verification

After executing a few instructions, hit the `GET /api/v1/memory` endpoint. Look for:
- **Execution Memory**: Contains history of strategies that succeeded or failed.
- **Capability Memory**: Contains frequency of tool usage.
- **Constraint Memory**: Lists dynamically learned boundaries (e.g., GitHub rate limits).
- **Learning Memory**: Displays optimization insights derived from past executions.

## 8. Learning Verification

To verify the system improves over time, query `GET /api/v1/metrics`. 
- **What to look for**: Repeated executions of identical or similar prompts should yield a higher `capability_reuse_rate`, lower `average_execution_time`, and potentially lower `average_api_calls` as the planner skips reasoning steps and relies on cached, learned paths.

## 9. Capability Synthesis Verification

1. First, check `GET /api/v1/capabilities`. You will see native tools (e.g., `create_issue` with `is_native=True`).
2. Run an unknown instruction (Demo 3).
3. Check `GET /api/v1/capabilities` again.
4. **Verification**: A new capability will appear with `creation_method: SYNTHESIS` and `is_native: False`. The `PlatformMindAppService` correctly tracks this dynamically generated tool for future reuse.

## 10. Partial Failure Testing

To verify error handling, intentionally cause a failure:
- **Invalid Repository**: Pass `"repository": "invalid/repository-name"`. 
- **Expected Behavior**: The API will return a structured JSON response under the `APIResponse` format indicating an execution failure. The `status` field in the `data` block will be `"FAILED"`, and the `failed_steps` or `errors` array will outline the HTTP 404 from GitHub.

## 11. API Response Structure

- **Execute**: Returns `ExecutionReportResponse`. Contains `execution_id`, the initial `instruction`, the detailed `execution_plan` (timeline), status, duration, and dynamically populated `metrics`.
- **Memory**: Returns `MemoryResponse`. Contains `execution_memory`, `capability_memory`, `constraint_memory`, and `learning_memory` dictionaries.
- **Reports**: Returns a list of `ExecutionReportResponse`.
- **Capabilities**: Returns a list of `CapabilityResponse` showing ID, name, description, version, creation method, and success rate.
- **Metrics**: Returns `MetricResponse` showing total executions, planner accuracy, time improvement percentages, and success trends.

## 12. Expected Assignment Mapping

| Requirement | Feature | Endpoint |
|------------|---------|---------|
| **1. Autonomous Execution** | Planner & Orchestrator | `POST /api/v1/execute` |
| **2. Persistent Memory** | Memory Engine | `GET /api/v1/memory` |
| **3. Learning Loop** | Metrics & Reasoning | `GET /api/v1/metrics` |
| **4. Capability Synthesis** | Synthesis Engine | `GET /api/v1/capabilities` |
| **5. Structured Reports** | Reporting Engine | `GET /api/v1/reports` |
| **6. Health Checks** | FastAPI Health Routers | `GET /api/health` |

## 13. Troubleshooting

- **Invalid GitHub Token**: If the system fails immediately on GitHub interactions, verify your Personal Access Token has `repo` (full control of private repositories) permissions.
- **Database Errors**: Delete `platformmind.db` in the root folder to wipe the SQLite database and restart the server to trigger a fresh migration.
- **Pydantic Validation Errors**: The LLM might occasionally output template variables (like `{{ issue_number }}`) instead of hard values. This is an LLM adherence issue; repeating the instruction usually circumvents it.
- **ModuleNotFoundError**: Ensure you are running commands using `uv run` to utilize the managed virtual environment.

## 14. Reviewer Checklist

As you evaluate the assignment, you can use this checklist to ensure every core feature is working as intended:

- [ ] ✅ Health endpoints working (`/api/health`)
- [ ] ✅ Execute endpoint working and returning structured standard API responses
- [ ] ✅ Planner successfully decomposes simple instructions
- [ ] ✅ GitHub API execution alters state on a test repository
- [ ] ✅ Memory persistence updates after execution (`/api/v1/memory`)
- [ ] ✅ Capability persistence tracks new synthesized tools
- [ ] ✅ Learning metrics report improvement percentages
- [ ] ✅ Structured reports generated with timestamps and metrics
- [ ] ✅ Partial failure handling intercepts errors gracefully
- [ ] ✅ Capability synthesis creates non-native tools dynamically
- [ ] ✅ Assignment completed fully

## 15. Comprehensive Test Scenarios (Dynamic Replanning)

To prove to Watermelon Software that PlatformMind is a robust, autonomous execution engine with dynamic replanning capabilities (Option 3), you can use the following comprehensive test suite. These scenarios validate the core requirements: **Autonomous ReAct Loop, Tool Routing, Context Building, and Resilience.**

### Core Autonomous Replanning (The ReAct Loop)
These tests prove that the system does not just generate a static list of tasks, but actively observes and reacts to data in real-time.

| Scenario | Instruction Payload | Expected Behavior & Proof |
| :--- | :--- | :--- |
| **Bulk Operation (Dynamic Spawning)** | `"Delete/Close all opened issues"` | **Iteration 1**: Executes `search_issues`.<br>**Iteration 2**: Dynamically spawns `N` individual `close_issue` tasks based on the search output.<br>**Iteration 3**: Terminates cleanly with an empty plan.<br>**Proof**: The execution response contains multiple iterations seamlessly grouped into one `ExecutionResult`. |
| **Chained Tool Execution** | `"Create a bug issue named 'Login Error' and label it 'high-priority'"` | **Iteration 1**: Executes `create_issue` and returns `issue_number: X`.<br>**Iteration 2**: Spawns `assign_label` and automatically resolves the `issue_number` dependency using the output from Iteration 1.<br>**Proof**: `assign_label` correctly targets the newly created issue. |

### Context Building & Dependency Resolution
These tests prove the `ContextBuilder` correctly manages state and execution outputs across steps.

| Scenario | Instruction Payload | Expected Behavior & Proof |
| :--- | :--- | :--- |
| **Implicit Reference Resolution** | `"Add the 'duplicate' label to the last issue we just created"` | The orchestrator accesses `previous_results` to find the issue number dynamically without the user explicitly stating it.<br>**Proof**: The `inputs` for `assign_label` are successfully resolved using `@step_id` or context fallbacks. |
| **Default Context Injection** | `"Find issues"` (No explicit query) | The system applies domain knowledge to inject a default query (`is:open is:issue`).<br>**Proof**: The executed `search_issues` step contains valid default inputs rather than crashing. |

### Resilience & Error Handling
These tests prove the platform is robust against bad inputs, hallucinations, and external API failures.

| Scenario | Instruction Payload | Expected Behavior & Proof |
| :--- | :--- | :--- |
| **Irrelevant / Out-of-Scope Task** | `"Order a pizza to my house"` | The `ToolSelector` fails to match the intent to any native capabilities. The planner returns a clean failure or prompts the synthesis engine without crashing the server.<br>**Proof**: HTTP 200/400 with a clear error payload (e.g. `unknown_tool`). |
| **External API Failure & Retry** | `"Create an issue" (simulate GitHub 503 error)` | The `ExecutionOrchestrator`'s retry manager kicks in. It attempts the operation up to 3 times with exponential backoff before failing the specific step.<br>**Proof**: `ExecutionResult` shows `retries > 0` and `failed_steps: ["step_x"]`. |
| **Partial Failure Handling** | `"Close issues #1 and #99999" (#99999 doesn't exist)` | The step for #1 succeeds, but #99999 fails (GitHub 404). The ReAct loop acknowledges the partial failure and exits gracefully.<br>**Proof**: `completed_steps` includes #1, `failed_steps` includes #99999, and the overall status is `COMPLETED` or `FAILED` (depending on strictness). |

### API Schema & Input Validation
These tests prove the API layer adheres strictly to OpenAPI/Pydantic validation schemas.

| Scenario | Instruction Payload | Expected Behavior & Proof |
| :--- | :--- | :--- |
| **Missing Required Field** | `{ "instruction": "search issues" }` (No `repository`) | FastAPI rejects the payload before it even hits the service layer.<br>**Proof**: HTTP 422 Unprocessable Entity indicating `repository` is missing. |
| **Invalid Repository Format** | `{ "instruction": "search issues", "repository": "invalid_format" }` | Pydantic regex validation fails because the string does not match `owner/repo`.<br>**Proof**: HTTP 422 Unprocessable Entity. |

### Execution Options
These tests prove the system respects user constraints and execution options.

| Scenario | Instruction Payload | Expected Behavior & Proof |
| :--- | :--- | :--- |
| **Dry Run Mode** | `"Close all issues"`, with `options: {"dry_run": true}` | The planner generates the exact ReAct loop tasks but the `ExecutionOrchestrator` skips the physical API calls.<br>**Proof**: Status is `COMPLETED`, but actual GitHub issues remain untouched. |

## 16. Conclusion

This project successfully fulfills the **Watermelon Software Autonomous Platform Intelligence Agent** assignment by implementing a multi-agent architectural pipeline. The system provides a highly polished API layer complete with strict Pydantic schemas, comprehensive structured reporting, a dynamic SQLite-backed memory engine, and an autonomous LLM capability synthesis framework. 

Thank you for reviewing PlatformMind!


---

## Appendix: Validating GitHub Assignment Requirements (Issues, PRs, Projects, Releases)

To prove to the recruiter that the agent can manage Issues, PRs, Projects, and Releases as per the assignment, you can run the following test cases. Note that tools not natively registered will dynamically trigger the `CapabilitySynthesisEngine` to compose new workflows.

### 1. Issue & Label Management (Native)
**Instruction:** "Create a high-priority bug report for the login timeout issue and assign it the 'bug' label."
- **Expected Behavior:** The planner will decompose this into `create_issue` and `assign_label`. It will execute both using the native GitHub tools.

### 2. Project/Milestone Management (Native)
**Instruction:** "Create a new milestone called 'Q3 MVP Launch'."
- **Expected Behavior:** The agent will execute this using the natively registered `create_milestone` tool.

### 3. Pull Request Management (Synthesis / Native Comments)
**Instruction:** "Add an LGTM comment to PR #12 and approve it."
- **Expected Behavior:** The agent will use the native `create_comment` tool for the comment. For the approval, the Synthesis engine will dynamically compose a new capability to interact with the GitHub PR Reviews API, sandbox test it, and execute it.

### 4. Releases Management (Synthesis)
**Instruction:** "Draft a new release for tag v0.2.0 titled 'Beta Release' with release notes."
- **Expected Behavior:** Detecting no native tool for `create_release`, the Synthesis engine will automatically generate the required GitHub REST API workflow, validate it, register it in Capability Memory, and create the release.
