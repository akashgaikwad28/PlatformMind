"""
Application settings and configuration.
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables or .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Application settings
    APP_NAME: str = "PlatformMind"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    DATABASE_URL: str = "sqlite+aiosqlite:///platformmind.db"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"

    GITHUB_TOKEN: str = ""
    GITHUB_OWNER: str = ""
    GITHUB_REPOSITORY: str = ""

    CHROMA_DB_PATH: str = "./data/chroma"

    LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"


settings = Settings()
