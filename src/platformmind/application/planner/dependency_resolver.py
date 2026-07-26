"""
Dependency Resolver.
"""

from typing import Any


class DependencyResolver:
    """
    Topologically sorts tasks to ensure dependencies execute first.
    """

    def resolve(self, tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        # Map task ID to task dict
        task_map = {t["id"]: t for t in tasks}

        # Build adjacency list
        graph = {t["id"]: set(t.get("depends_on", [])) for t in tasks}

        sorted_tasks = []
        visited = set()
        temp_marked = set()

        def visit(n: str) -> None:
            if n in temp_marked:
                raise ValueError("Circular dependency detected in tasks")
            if n not in visited:
                temp_marked.add(n)
                for m in graph.get(n, []):
                    visit(m)
                temp_marked.remove(n)
                visited.add(n)
                if n in task_map:
                    sorted_tasks.append(task_map[n])

        for node in graph:
            if node not in visited:
                visit(node)

        return sorted_tasks
