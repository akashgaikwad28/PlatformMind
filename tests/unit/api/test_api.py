from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from platformmind.api.app import create_app
from platformmind.api.dependencies import (
    get_capabilities_engine,
    get_execution_engine,
    get_memory_engine,
    get_metrics_engine,
    get_reporting_engine,
)


class MockExecutionEngine:
    def execute(self, instruction, repo, options):
        return "exec_123"


class MockMemoryEngine:
    def get_memory(self):
        return {"execution": {}, "capabilities": {}, "constraints": {}, "learning": {}}


class MockCapabilitiesEngine:
    def get_capabilities(self):
        return [
            {
                "id": "cap_1",
                "name": "Test Cap",
                "description": "desc",
                "version": "1.0",
                "creation_method": "NATIVE",
                "is_native": True,
                "usage_count": 0,
                "success_rate": 1.0,
                "average_execution_time": 0.0,
                "confidence": 1.0,
                "created_at": "2026-07-25T00:00:00Z",
                "last_used": None,
                "dependencies": [],
                "status": "ACTIVE",
            }
        ]


class MockReportingEngine:
    def get_reports(self):
        return []


class MockMetricsEngine:
    def get_metrics(self):
        return {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "average_execution_time": 0.0,
            "average_api_calls": 0.0,
            "retry_rate": 0.0,
            "capability_reuse_rate": 0.0,
            "capability_synthesis_count": 0,
            "planner_accuracy": 1.0,
            "time_improvement_pct": 0.0,
            "calls_improvement_pct": 0.0,
            "memory_size": 0,
            "constraints_learned": 0,
            "success_trend": [],
            "tool_usage": {},
            "most_common_instruction": None,
        }


@pytest.fixture
def client() -> Any:
    app = create_app()
    app.dependency_overrides[get_execution_engine] = lambda: MockExecutionEngine()
    app.dependency_overrides[get_memory_engine] = lambda: MockMemoryEngine()
    app.dependency_overrides[get_capabilities_engine] = lambda: MockCapabilitiesEngine()
    app.dependency_overrides[get_reporting_engine] = lambda: MockReportingEngine()
    app.dependency_overrides[get_metrics_engine] = lambda: MockMetricsEngine()
    return TestClient(app)


def test_health_probes(client) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200

    response = client.get("/api/ready")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ready"

    response = client.get("/api/live")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "alive"


def test_execution_endpoint_success(client) -> None:
    payload = {"instruction": "Do something", "repository": "my-org/my-repo"}
    response = client.post("/api/v1/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "execution_id" in data["data"]
    assert "request_id" in data


def test_execution_endpoint_validation_error(client) -> None:
    payload = {"repository": "my-org/my-repo"}
    response = client.post("/api/v1/execute", json=payload)
    assert response.status_code == 422


def test_memory_endpoint(client) -> None:
    response = client.get("/api/v1/memory")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "execution" in data["data"]["execution_memory"] or isinstance(
        data["data"]["execution_memory"], dict
    )


def test_capabilities_endpoint(client) -> None:
    response = client.get("/api/v1/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) > 0
    assert data["data"][0]["id"] == "cap_1"


def test_reports_endpoint(client) -> None:
    response = client.get("/api/v1/reports")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_metrics_endpoint(client) -> None:
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["total_executions"] == 0


def test_real_container_endpoints() -> None:
    app = create_app()
    with TestClient(app) as real_client:
        with patch.object(
            real_client.app.state.execution_engine, "execute", new_callable=AsyncMock
        ) as p_exec:
            p_exec.return_value = "exec_test123"

            response = real_client.get("/api/v1/reports")
            assert response.status_code == 200

            response = real_client.get("/api/v1/memory")
            assert response.status_code == 200

            response = real_client.get("/api/v1/capabilities")
            assert response.status_code == 200

            response = real_client.get("/api/v1/metrics")
            assert response.status_code == 200

            response = real_client.get("/api/v1/synthesis/history")
            assert response.status_code == 200

            payload = {"instruction": "Refactor code", "repository": "test/repo"}
            response = real_client.post("/api/v1/execute", json=payload)
            assert response.status_code == 200
            assert response.json()["status"] == "success"
            assert response.json()["data"]["execution_id"] == "exec_test123"
