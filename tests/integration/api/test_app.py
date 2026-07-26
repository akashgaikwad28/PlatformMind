import pytest

from platformmind.api.app import create_app


@pytest.mark.asyncio
async def test_app_startup() -> None:
    """Test that the FastAPI application can be created successfully."""
    app = create_app()
    assert app is not None
    assert app.title == "PlatformMind"
