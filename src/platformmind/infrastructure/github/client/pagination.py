"""
Pagination Helpers.
"""

from typing import Any

from platformmind.infrastructure.github.client.client import GitHubClient


class PaginationHelper:
    """
    Handles automatic pagination for GitHub list endpoints.
    """

    @staticmethod
    async def paginate(
        client: GitHubClient, path: str, params: dict | None = None
    ) -> list[Any]:
        """
        Eagerly fetches all pages (simple implementation).
        In a real scenario, this would yield an async generator or parse 'Link' headers.
        """
        if params is None:
            params = {}

        all_results = []
        page = 1
        per_page = 100
        params["per_page"] = per_page

        while True:
            params["page"] = page
            data, status = await client.get(path, params=params)
            if not isinstance(data, list):
                # Endpoint does not return a list, can't paginate
                return data if data else []

            all_results.extend(data)

            if len(data) < per_page:
                break
            page += 1

        return all_results
