"""
GitHub API Mappers.
"""
# Assuming domain models for issue/label/comment exist, or mapping directly.
# Since phase 5 requires SDK-like return, we usually map JSON to Pydantic if needed.
# Let's provide a generic mapper structure.

from typing import Any


class GitHubMapper:
    """
    Converts raw GitHub API JSON into structured internal/domain models.
    """

    @staticmethod
    def map_issue(data: dict[str, Any]) -> dict[str, Any]:
        """Maps raw issue JSON to a cleaner structure without leaking GitHub specifics"""
        return {
            "id": data.get("id"),
            "number": data.get("number"),
            "title": data.get("title"),
            "state": data.get("state"),
            "labels": [
                lbl["name"] for lbl in data.get("labels", []) if isinstance(lbl, dict)
            ],
            "url": data.get("html_url"),
        }
