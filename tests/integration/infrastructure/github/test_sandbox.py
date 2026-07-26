import os
from typing import Any

import pytest

from platformmind.infrastructure.github.client.client import GitHubClient
from platformmind.infrastructure.github.tools.issues import (
    CloseIssueTool,
    CreateIssueTool,
)

# Skip if credentials are not available
pytestmark = pytest.mark.skipif(
    not os.getenv("GITHUB_TOKEN") or not os.getenv("GITHUB_OWNER"),
    reason="Sandbox credentials not set",
)


@pytest.fixture
def sandbox_client() -> Any:
    token = os.getenv("GITHUB_TOKEN", "dummy")
    owner = os.getenv("GITHUB_OWNER", "dummy")
    repo = os.getenv("GITHUB_REPOSITORY", "dummy")
    return GitHubClient(token=token, owner=owner, repo=repo)


@pytest.mark.asyncio
async def test_sandbox_issue_lifecycle(sandbox_client) -> None:
    """
    Creates an issue and immediately closes it.
    """
    create_tool = CreateIssueTool(sandbox_client)
    res = await create_tool.run(
        title="Sandbox Test Issue", body="Testing issue lifecycle"
    )

    assert res.success is True, f"Failed to create issue: {res.errors}"
    assert res.status_code == 201

    issue_number = res.data["number"]

    close_tool = CloseIssueTool(sandbox_client)
    close_res = await close_tool.run(issue_number=issue_number)

    assert close_res.success is True
    assert close_res.status_code == 200
    assert close_res.data["state"] == "closed"
