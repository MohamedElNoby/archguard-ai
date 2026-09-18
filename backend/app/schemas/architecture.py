"""Pydantic schemas for the ArchitectureSpec entity.

`ArchitectureIngest` is the STABLE JSON CONTRACT the AI/orchestration
teammate's Gemini layer (or any future LLM provider) must send to this
backend. Keeping `provider`/`model` optional and `raw_analysis` permissive
(dict[str, Any]) means new AI providers or evolving prompt outputs never
require a schema change here.
"""
from __future__ import annotations

import datetime as dt
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ArchitectureData(BaseModel):
    """The structured architecture payload itself."""

    components: list[str] = Field(
        default_factory=list,
        description="List of architecture component names, e.g. ['Frontend', 'FastAPI']",
    )
    routes: list[list[str]] = Field(
        default_factory=list,
        description="List of [source, target] connections, e.g. [['Frontend', 'FastAPI']]",
    )

    @field_validator("routes")
    @classmethod
    def _validate_routes(cls, routes: list[list[str]]) -> list[list[str]]:
        for route in routes:
            if len(route) != 2:
                raise ValueError(
                    "Each route must be a [source, target] pair, "
                    f"got {route!r} with {len(route)} elements"
                )
        return routes


class ArchitectureIngest(BaseModel):
    """
    Payload accepted from the AI/orchestration layer (or mock fixtures) to
    create/replace the ArchitectureSpec for a project.

    Example:
    {
        "provider": "gemini",
        "model": "gemini-2.5-pro",
        "architecture": {
            "components": ["Frontend", "FastAPI", "PostgreSQL"],
            "routes": [["Frontend", "FastAPI"], ["FastAPI", "PostgreSQL"]]
        },
        "raw_analysis": { ... full original AI response, optional ... }
    }
    """

    provider: Optional[str] = Field(default=None, max_length=100)
    model: Optional[str] = Field(default=None, max_length=150)
    architecture: ArchitectureData
    raw_analysis: Optional[dict[str, Any]] = Field(
        default=None,
        description="Optional full/raw AI response for auditing purposes",
    )


class ArchitectureUpdate(BaseModel):
    """Payload for partially updating an existing ArchitectureSpec."""

    provider: Optional[str] = Field(default=None, max_length=100)
    model: Optional[str] = Field(default=None, max_length=150)
    architecture: Optional[ArchitectureData] = None
    raw_analysis: Optional[dict[str, Any]] = None


class ArchitectureRead(BaseModel):
    """Full ArchitectureSpec representation returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    components: list[str]
    routes: list[list[str]]
    raw_analysis: Optional[dict[str, Any]] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    created_at: dt.datetime
    updated_at: dt.datetime