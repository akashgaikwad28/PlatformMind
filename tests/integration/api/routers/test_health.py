import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(app_client: AsyncClient) -> None:
    """Test that the health endpoint returns the expected response."""
    response = await app_client.get("/api/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    inner_data = data["data"]
    assert inner_data["status"] in ["healthy", "degraded"]
    assert "application" in inner_data
    assert "version" in inner_data
    assert "environment" in inner_data
    assert "timestamp" in inner_data
