import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(app_client: AsyncClient):
    response = await app_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["status"] in ["healthy", "degraded"]
    assert "application" in data["data"]
    assert "components" in data["data"]


@pytest.mark.asyncio
async def test_readiness_probe(app_client: AsyncClient):
    response = await app_client.get("/api/ready")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ready"


@pytest.mark.asyncio
async def test_liveness_probe(app_client: AsyncClient):
    response = await app_client.get("/api/live")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "alive"


@pytest.mark.asyncio
async def test_validation_error_format(app_client: AsyncClient):
    # Missing required fields
    response = await app_client.post("/api/v1/execute", json={"instruction": ""})
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "instruction" in str(data["error"]["details"])


@pytest.mark.asyncio
async def test_metrics_endpoint(app_client: AsyncClient):
    response = await app_client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "total_executions" in data["data"]


@pytest.mark.asyncio
async def test_capabilities_endpoint(app_client: AsyncClient):
    response = await app_client.get("/api/v1/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_memory_endpoint(app_client: AsyncClient):
    response = await app_client.get("/api/v1/memory")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "execution_memory" in data["data"]
    assert "capability_memory" in data["data"]


@pytest.mark.asyncio
async def test_reports_endpoint(app_client: AsyncClient):
    response = await app_client.get("/api/v1/reports")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_synthesis_history_endpoint(app_client: AsyncClient):
    response = await app_client.get("/api/v1/synthesis/history")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_single_report_not_found(app_client: AsyncClient):
    response = await app_client.get("/api/v1/reports/non_existent_id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_404_not_found(app_client: AsyncClient):
    response = await app_client.get("/api/v1/invalid_endpoint")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_405_method_not_allowed(app_client: AsyncClient):
    response = await app_client.post("/api/v1/metrics")
    assert response.status_code == 405
