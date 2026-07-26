import pytest

from platformmind.core.config.settings import Settings


def test_settings_loading(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that settings load correctly from environment variables."""
    monkeypatch.setenv("APP_NAME", "TestApp")
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("REQUEST_TIMEOUT", "10")

    settings = Settings()

    assert settings.APP_NAME == "TestApp"
    assert settings.APP_ENV == "testing"
    assert settings.REQUEST_TIMEOUT == 10


def test_settings_validation_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that invalid settings raise validation errors."""
    monkeypatch.setenv("REQUEST_TIMEOUT", "invalid_int")

    with pytest.raises(ValueError):
        Settings()
