"""Low-level CRUD operations for the Project model.

These functions only talk to the database session - no HTTP concerns
(status codes, exceptions meant for FastAPI) live here. That logic belongs
in app/services/project_service.py.
"""
from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def create_project(db: Session, payload: ProjectCreate) -> Project:
    project = Project(
        name=payload.name,
        description=payload.description,
        diagram_path=payload.diagram_path,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_project(db: Session, project_id: str) -> Optional[Project]:
    return db.get(Project, project_id)


def list_projects(db: Session, skip: int = 0, limit: int = 100) -> list[Project]:
    stmt = (
        select(Project)
        .order_by(Project.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().all())


def count_projects(db: Session) -> int:
    return db.query(Project).count()


def update_project(
    db: Session, project: Project, payload: ProjectUpdate
) -> Project:
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()
