---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/application/interfaces/execution/tool.py`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Adding a GitHub Tool

## Purpose
Guide to extending the agent's capability to interact with GitHub.

## Internal Workflow

### 1. Create the Tool Class
Inherit from `BaseTool`. Create it in `src/platformmind/application/tools/github/`.

```python
from pydantic import BaseModel, Field
from platformmind.application.interfaces.execution.tool import BaseTool

class AddLabelInputs(BaseModel):
    repo: str = Field(description="Format: owner/repo")
    issue_number: int = Field(description="Issue number")
    labels: list[str] = Field(description="Labels to apply")

class AddLabelTool(BaseTool):
    name = "add_github_label"
    description = "Applies labels to an existing GitHub issue or PR."
    inputs_schema = AddLabelInputs
    
    async def run(self, inputs: dict) -> dict:
        parsed = self.inputs_schema(**inputs)
        # 1. Fetch GitHub client from DI or context
        # 2. Make API Call
        # 3. Return results dict
        return {"success": True, "added": parsed.labels}
        
    async def rollback(self, inputs: dict, result: dict) -> None:
        # Implement logic to remove the labels if the DAG fails later
        pass
```

### 2. Register the Tool
Open `src/platformmind/application/execution/tool_registry.py` and register the new tool in the `__init__` or startup hook.

### 3. Update Capabilities (Optional)
If this tool implies a new standard capability, you can seed it into the database, or simply let the Planner synthesize it at runtime.

## Important Considerations
- **Docstrings and Descriptions:** The `description` field and Pydantic `Field` descriptions are directly injected into the LLM prompt. Be incredibly precise about what the tool does and what format it expects.
- **Rollback:** Always implement `rollback` for destructive actions.
