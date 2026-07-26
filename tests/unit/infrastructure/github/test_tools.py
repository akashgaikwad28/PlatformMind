from unittest.mock import AsyncMock

import pytest

from platformmind.infrastructure.github.tools.issues import CreateIssueTool


@pytest.mark.asyncio
async def test_create_issue_tool_validation() -> None:
    tool = CreateIssueTool(client=AsyncMock())

    # Missing title
    res = await tool.run(body="hello")
    assert res.success is False
    assert len(res.errors) > 0
    assert "title" in res.errors[0].lower() or "missing" in res.errors[0].lower()


@pytest.mark.asyncio
async def test_create_issue_tool_success() -> None:
    mock_client = AsyncMock()
    mock_client.post.return_value = ({"id": 1, "title": "Test"}, 201)
    mock_client.owner = "test"
    mock_client.repo = "repo"

    tool = CreateIssueTool(client=mock_client)
    res = await tool.run(title="Test", body="body")

    assert res.success is True
    assert res.data["title"] == "Test"
    assert res.api_calls == 1
    assert res.status_code == 201
