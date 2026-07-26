---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/application/planner/pipeline.py`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Adding a Planner Stage

## Purpose
Guide to extending the NLP reasoning pipeline.

## Internal Workflow

### 1. Create the Stage
Create a class implementing the `PipelineStage` interface (if defined, or simply a callable object).

```python
class SensitiveDataFilterStage:
    def __init__(self, vault_client):
        self.vault = vault_client
        
    async def execute(self, context: dict) -> dict:
        instruction = context["instruction"]
        # Find and replace sensitive data
        context["instruction"] = sanitize(instruction)
        return context
```

### 2. Inject into the Pipeline
Open `src/platformmind/application/planner/pipeline.py` and add the stage into the sequence array in `__init__`.

```python
self.stages = [
    InstructionNormalizer(),
    SensitiveDataFilterStage(vault), # New Stage
    IntentClassifier(),
    # ...
]
```

## Important Considerations
- Pipeline stages modify the shared `context` dictionary. Avoid mutating variables that downstream stages rely on unless intentionally modifying behavior.
