"""Pydantic schemas for the Project entity."""
from __future__ import annotations

import datetime as dt
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(
        default=None, max_length=5000, description="Optional free-text description"
    )
    diagram_path: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Path/URL to the uploaded architecture diagram or ERD image",
    )


class ProjectCreate(ProjectBase):
    """Payload for creating a new project."""

    pass


class ProjectUpdate(BaseModel):
    """Payload for partially updating a project. All fields optional."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=5000)
    diagram_path: Optional[str] = Field(default=None, max_length=500)
    status: Optional[str] = Field(default=None, max_length=50)


class ProjectRead(ProjectBase):
    """Full project representation returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    status: str
    created_at: dt.datetime
    updated_at: dt.datetime


class ProjectListResponse(BaseModel):
    """Paginated-ready list wrapper (simple count + items for the hackathon)."""

    count: int
    items: list[ProjectRead]
