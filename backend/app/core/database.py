"""
Database engine, session factory, and declarative base.

Designed so that swapping SQLite for PostgreSQL later only requires changing
the DATABASE_URL environment variable - nothing here is SQLite-specific
except the `connect_args` tweak needed for SQLite + multithreaded FastAPI.
"""
from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# SQLite needs `check_same_thread=False` to be used safely across the
# request threads that FastAPI's threadpool may spin up. Other databases
# (e.g. PostgreSQL) do not need or support this argument.
connect_args = {"check_same_thread": False} if settings.is_sqlite else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    future=True,
)


# Enforce SQLite foreign-key constraints (off by default in SQLite).
if settings.is_sqlite:

    @event.listens_for(Engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record) -> None:  # noqa: ANN001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
)


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""

    pass


def init_db() -> None:
    """Create all database tables if they do not already exist.

    Importing the models module here (rather than at module load time)
    avoids circular imports while still guaranteeing that every model is
    registered on `Base.metadata` before `create_all` runs.
    """
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    """FastAPI dependency that yields a database session per-request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
