"""
Context Builder.
"""

import uuid
from datetime import datetime
from typing import Any

from platformmind.domain.models.instruction import Instruction
from platformmind.domain.models.planning_context import PlanningContext


class ContextBuilder:
    """
    Assembles the complete execution context before planning begins.
    Does not perform live API lookups (that is reserved for the RepositoryContextProvider).
    """

    def build(
        self, instruction: Instruction, repository: str, options: dict[str, Any]
    ) -> PlanningContext:
        """
        Builds the PlanningContext from raw instruction and options.
        """
        # Parse repository details
        owner = "unknown"
        name = repository

        # Strip potential URLs
        clean_repo = repository
        if clean_repo.startswith("https://github.com/"):
            clean_repo = clean_repo.replace("https://github.com/", "")
        if clean_repo.endswith(".git"):
            clean_repo = clean_repo[:-4]

        parts = clean_repo.split("/")
        if len(parts) == 2:
            owner = parts[0]
            name = parts[1]

        dry_run = options.get("dry_run", False)

        return PlanningContext(
            instruction=instruction,
            repository=repository,
            repository_owner=owner,
            repository_name=name,
            repository_type="github",
            repository_permissions=options.get("permissions", {}),
            options=options,
            dry_run=dry_run,
            current_timestamp=datetime.utcnow().isoformat(),
            session_id=options.get("session_id", uuid.uuid4().hex),
            previous_execution_id=options.get("previous_execution_id"),
            environment=options.get("environment", "production"),
            llm_configuration=options.get("llm_configuration", {}),
            runtime_configuration=options.get("runtime_configuration", {}),
        )
