import pytest
from httpx import ASGITransport, AsyncClient

from platformmind.api.app import create_app
from platformmind.api.dependencies import (
    get_capabilities_engine,
    get_execution_engine,
    get_memory_engine,
    get_metrics_engine,
    get_reporting_engine,
)


class MockExecutionEngine:
    async def execute(self, instruction, repo, options):
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
async def app_client():
    app = create_app()
    app.dependency_overrides[get_execution_engine] = lambda: MockExecutionEngine()
    app.dependency_overrides[get_memory_engine] = lambda: MockMemoryEngine()
    app.dependency_overrides[get_capabilities_engine] = lambda: MockCapabilitiesEngine()
    app.dependency_overrides[get_reporting_engine] = lambda: MockReportingEngine()
    app.dependency_overrides[get_metrics_engine] = lambda: MockMetricsEngine()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
