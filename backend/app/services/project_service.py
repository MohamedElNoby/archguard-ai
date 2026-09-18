"""Service layer for Project: wraps CRUD calls with HTTP-appropriate errors.

Keeping this layer separate from `app/crud` means the CRUD functions stay
framework-agnostic (pure SQLAlchemy), while this layer is responsible for
translating "not found" into a 404, etc.
"""
from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import project as project_crud
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def create_project(db: Session, payload: ProjectCreate) -> Project:
    return project_crud.create_project(db, payload)


def get_project_or_404(db: Session, project_id: str) -> Project:
    project = project_crud.get_project(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_id}' not found.",
        )
    return project


def list_projects(db: Session, skip: int = 0, limit: int = 100) -> tuple[list[Project], int]:
    items = project_crud.list_projects(db, skip=skip, limit=limit)
    total = project_crud.count_projects(db)
    return items, total


def update_project(db: Session, project_id: str, payload: ProjectUpdate) -> Project:
    project = get_project_or_404(db, project_id)
    return project_crud.update_project(db, project, payload)


def delete_project(db: Session, project_id: str) -> None:
    project = get_project_or_404(db, project_id)
    project_crud.delete_project(db, project)
