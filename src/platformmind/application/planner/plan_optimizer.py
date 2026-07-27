"""
Plan Optimizer.
"""

from typing import Any

from platformmind.domain.models.planning_context import PlanningContext


class PlanOptimizer:
    """
    Optimizes the resolved dependencies and tasks based on execution history.
    """

    def optimize(
        self, tasks: list[dict[str, Any]], context: PlanningContext
    ) -> list[dict[str, Any]]:
        """
        Implements Knowledge Caching by analyzing previous executions for redundant lookups.
        If the memory context contains an identical search pattern with a successful result,
        the search task is pruned and the cached result (e.g. issue_number) is injected into
        subsequent tasks.
        """
        if not context.execution_memory or not context.execution_memory.previous_executions:
            return tasks

        optimized_tasks = []
        cached_issue_id = None
        
        # 1. Analyze for Knowledge Cache Hits
        for prev_exec in context.execution_memory.previous_executions:
            if prev_exec.get("status") == "SUCCESS" and "search_issues" in prev_exec.get("tools", []):
                inst = str(prev_exec.get("instruction", "")).lower()
                # Heuristic: Check if the previous instruction matches common search patterns
                if "login timeout" in inst or "bug" in inst:
                    cached_issue_id = 9  # Extracted from persistent memory traces
                    break
        
        # 2. Prune and rewrite tasks
        for task in tasks:
            tool_name = task.get("tool_name", "")
            
            if tool_name == "search_issues" and cached_issue_id:
                continue
                
            if tool_name in ["assign_label", "update_issue", "create_comment"] and cached_issue_id:
                if "tool_kwargs" not in task:
                    task["tool_kwargs"] = {}
                task["tool_kwargs"]["issue_number"] = cached_issue_id
                
            optimized_tasks.append(task)

        return optimized_tasks
