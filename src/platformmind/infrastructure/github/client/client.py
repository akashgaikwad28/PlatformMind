"""
GitHub API Client.
"""

import asyncio
from typing import Any

import httpx

from platformmind.infrastructure.github.exceptions.exceptions import (
    GitHubConflictError,
    GitHubConnectionError,
    GitHubError,
    GitHubForbiddenError,
    GitHubNotFoundError,
    GitHubRateLimitError,
    GitHubServerError,
    GitHubUnauthorizedError,
    GitHubValidationError,
)


class GitHubClient:
    """
    Reusable GitHub REST API client using httpx.AsyncClient.
    """

    def __init__(
        self,
        token: str,
        owner: str,
        repo: str,
        base_url: str = "https://api.github.com",
    ):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = base_url
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github.v3+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=10.0,
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
        )

    async def close(self) -> None:
        await self._client.aclose()

    def _handle_response(self, response: httpx.Response) -> Any:
        if 200 <= response.status_code < 300:
            return response.json() if response.content else None

        # Handle specific errors
        if response.status_code == 401:
            raise GitHubUnauthorizedError(f"Unauthorized: {response.text}")
        elif response.status_code == 403:
            # Check for rate limit specifically
            if "rate limit" in response.text.lower():
                reset = int(response.headers.get("X-RateLimit-Reset", 0))
                raise GitHubRateLimitError("Rate limit exceeded", reset_time=reset)
            raise GitHubForbiddenError(f"Forbidden: {response.text}")
        elif response.status_code == 404:
            raise GitHubNotFoundError(f"Not Found: {response.text}")
        elif response.status_code == 409:
            raise GitHubConflictError(f"Conflict: {response.text}")
        elif response.status_code == 422:
            raise GitHubValidationError(f"Validation Error: {response.text}")
        elif response.status_code >= 500:
            raise GitHubServerError(
                f"Server Error ({response.status_code}): {response.text}"
            )

        raise GitHubError(f"API Error ({response.status_code}): {response.text}")

    async def _request_with_retry(
        self, method: str, url: str, **kwargs: Any
    ) -> tuple[Any, int]:
        retries = 3
        for attempt in range(retries):
            try:
                response = await self._client.request(method, url, **kwargs)
                data = self._handle_response(response)
                return data, response.status_code
            except GitHubRateLimitError:
                # Basic backoff if we hit rate limits (naive implementation for demo)
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(2**attempt)
            except (httpx.TimeoutException, httpx.NetworkError) as e:
                if attempt == retries - 1:
                    raise GitHubConnectionError(f"Connection failed: {str(e)}") from e
                await asyncio.sleep(2**attempt)
            except GitHubError:
                raise  # Don't retry client/validation errors

        raise GitHubError("Max retries exceeded")

    async def get(self, path: str, params: dict | None = None) -> tuple[Any, int]:
        return await self._request_with_retry("GET", path, params=params)

    async def post(self, path: str, json: dict | None = None) -> tuple[Any, int]:
        return await self._request_with_retry("POST", path, json=json)

    async def patch(self, path: str, json: dict | None = None) -> tuple[Any, int]:
        return await self._request_with_retry("PATCH", path, json=json)

    async def put(self, path: str, json: dict | None = None) -> tuple[Any, int]:
        return await self._request_with_retry("PUT", path, json=json)

    async def delete(self, path: str) -> tuple[Any, int]:
        return await self._request_with_retry("DELETE", path)
