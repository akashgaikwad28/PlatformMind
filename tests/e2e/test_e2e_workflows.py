from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient


@pytest.fixture
def mock_github_and_llm():
    with (
        patch(
            "platformmind.infrastructure.github.client.client.GitHubClient.post",
            new_callable=AsyncMock,
        ) as mock_gh_post,
        patch(
            "platformmind.infrastructure.github.client.client.GitHubClient.get",
            new_callable=AsyncMock,
        ) as mock_gh_get,
        patch(
            "platformmind.infrastructure.llm.groq_provider.GroqProvider.generate",
            new_callable=AsyncMock,
        ) as mock_llm_gen,
        patch(
            "platformmind.infrastructure.llm.groq_provider.GroqProvider.embed",
            new_callable=AsyncMock,
        ) as mock_llm_embed,
    ):
        # Setup mocks
        mock_gh_post.return_value = (
            {"html_url": "https://github.com/mock/repo/issues/1", "number": 1},
            201,
        )
        mock_gh_get.return_value = ({"status": "ok"}, 200)

        # We mock LLM to return valid JSON for the planner depending on the prompt
        # For simplicity, we just patch the AppService entirely in the tests below,
        # but this fixture demonstrates how we'd mock the lowest levels if we ran the real pipeline.
        mock_llm_embed.return_value = [0.1] * 1536
        yield mock_gh_post, mock_llm_gen


@pytest.fixture
def mock_app_service():
    with patch("platformmind.api.container.PlatformMindAppService") as MockService:
        service_instance = MockService.return_value
        service_instance.execute = AsyncMock(return_value="exec_123")
        yield service_instance


@pytest.mark.asyncio
async def test_demo_1_simple_github_issue(app_client: AsyncClient, mock_app_service):
    # Simulate an instruction
    payload = {
        "instruction": "Create a GitHub issue titled 'Login bug'",
        "repository": "mock/repo",
    }

    # Executing
    response = await app_client.post("/api/v1/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    # Ensure our API correctly structured the mock report
    # (the API gracefully builds a fallback report if reporting engine is missing the ID)
    assert "execution_id" in data["data"]
    assert data["data"]["instruction"] == payload["instruction"]
    assert "metrics" in data["data"]


@pytest.mark.asyncio
async def test_demo_2_compound_instruction(app_client: AsyncClient, mock_app_service):
    payload = {
        "instruction": "Find open bugs and assign them the 'triage' label",
        "repository": "mock/repo",
    }
    response = await app_client.post("/api/v1/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "execution_id" in data["data"]


@pytest.mark.asyncio
async def test_demo_3_unknown_instruction_synthesis(
    app_client: AsyncClient, mock_app_service
):
    payload = {
        "instruction": "Perform a completely unknown action requiring synthesis",
        "repository": "mock/repo",
    }
    response = await app_client.post("/api/v1/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "execution_id" in data["data"]
