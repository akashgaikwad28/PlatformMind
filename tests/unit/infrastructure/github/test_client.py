from typing import Any
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from platformmind.infrastructure.github.client.client import GitHubClient
from platformmind.infrastructure.github.exceptions.exceptions import (
    GitHubRateLimitError,
    GitHubUnauthorizedError,
)


@pytest.fixture
def github_client() -> Any:
    return GitHubClient(token="fake", owner="test", repo="testrepo")


@pytest.mark.asyncio
async def test_github_client_unauthorized(github_client) -> None:
    mock_response = httpx.Response(401, text="Bad credentials")

    with patch.object(
        github_client._client, "request", new_callable=AsyncMock
    ) as mock_req:
        mock_req.return_value = mock_response

        with pytest.raises(GitHubUnauthorizedError):
            await github_client.get("/user")


@pytest.mark.asyncio
async def test_github_client_rate_limit(github_client) -> None:
    mock_response = httpx.Response(
        403, text="API rate limit exceeded", headers={"X-RateLimit-Reset": "1234567890"}
    )

    with patch.object(
        github_client._client, "request", new_callable=AsyncMock
    ) as mock_req:
        mock_req.return_value = mock_response

        with pytest.raises(GitHubRateLimitError) as exc:
            await github_client.get("/user")
        assert exc.value.reset_time == 1234567890


@pytest.mark.asyncio
async def test_github_client_success(github_client) -> None:
    mock_response = httpx.Response(200, json={"login": "octocat"})

    with patch.object(
        github_client._client, "request", new_callable=AsyncMock
    ) as mock_req:
        mock_req.return_value = mock_response

        data, status = await github_client.get("/user")
        assert status == 200
        assert data["login"] == "octocat"
