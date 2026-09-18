"""REST endpoints for the Project entity.

NOTE: Image upload (multipart) + Gemini analysis kick-off belongs to the
"Backend Core & Orchestration" teammate and is intentionally NOT implemented
here (e.g. no `POST /api/v1/projects/upload`). This router only owns plain
CRUD over project metadata.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.project import (
    ProjectCreate,
    ProjectListResponse,
    ProjectRead,
    ProjectUpdate,
)
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> ProjectRead:
    project = project_service.create_project(db, payload)
    return ProjectRead.model_validate(project)


@router.get(
    "",
    response_model=ProjectListResponse,
    summary="List all projects",
)
def list_projects(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> ProjectListResponse:
    items, total = project_service.list_projects(db, skip=skip, limit=limit)
    return ProjectListResponse(
        count=total, items=[ProjectRead.model_validate(p) for p in items]
    )


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Get a single project by ID",
)
def get_project(project_id: str, db: Session = Depends(get_db)) -> ProjectRead:
    project = project_service.get_project_or_404(db, project_id)
    return ProjectRead.model_validate(project)


@router.put(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Update a project",
)
def update_project(
    project_id: str, payload: ProjectUpdate, db: Session = Depends(get_db)
) -> ProjectRead:
    project = project_service.update_project(db, project_id, payload)
    return ProjectRead.model_validate(project)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Delete a project (cascades to its ArchitectureSpec/RiskAssessment)",
)
def delete_project(project_id: str, db: Session = Depends(get_db)) -> None:
    project_service.delete_project(db, project_id)
    return None
