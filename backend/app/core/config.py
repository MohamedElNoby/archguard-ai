"""
Application configuration.

All configuration is loaded from environment variables (with sane defaults
for local development), so the app can move from SQLite to PostgreSQL later
by only changing DATABASE_URL - no application code changes required.
"""
from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv

# Load variables from a .env file if present (no-op if it doesn't exist).
load_dotenv()


class Settings:
    """Simple settings object populated from environment variables."""

    # --- Database -----------------------------------------------------
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./archredteam.db")

    # --- App metadata ---------------------------------------------------
    APP_NAME: str = os.getenv("APP_NAME", "AI ArchRedTeam - Database & State API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")

    # --- Misc ------------------------------------------------------------
    DEBUG: bool = os.getenv("DEBUG", "true").lower() in {"1", "true", "yes"}

    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_URL.startswith("sqlite")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (avoids re-reading env vars)."""
    return Settings()


settings = get_settings()
