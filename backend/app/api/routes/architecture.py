"""REST endpoints for the ArchitectureSpec entity.

These endpoints are the integration point for the AI/orchestration
teammate: after Gemini (or any provider) analyzes an uploaded diagram, that
teammate's code should POST the result here using the `ArchitectureIngest`
contract (see app/schemas/architecture.py).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.architecture import (
    ArchitectureIngest,
    ArchitectureRead,
    ArchitectureUpdate,
)
from app.services import architecture_service

router = APIRouter(prefix="/projects/{project_id}/architecture", tags=["Architecture"])


@router.post(
    "",
    response_model=ArchitectureRead,
    status_code=status.HTTP_201_CREATED,
    summary="Store the AI-generated architecture spec for a project",
)
def create_architecture(
    project_id: str, payload: ArchitectureIngest, db: Session = Depends(get_db)
) -> ArchitectureRead:
    spec = architecture_service.create_architecture_spec(db, project_id, payload)
    return ArchitectureRead.model_validate(spec)


@router.get(
    "",
    response_model=ArchitectureRead,
    summary="Get the architecture spec for a project",
)
def get_architecture(project_id: str, db: Session = Depends(get_db)) -> ArchitectureRead:
    spec = architecture_service.get_architecture_by_project_or_404(db, project_id)
    return ArchitectureRead.model_validate(spec)


@router.put(
    "",
    response_model=ArchitectureRead,
    summary="Update the architecture spec for a project",
)
def update_architecture(
    project_id: str, payload: ArchitectureUpdate, db: Session = Depends(get_db)
) -> ArchitectureRead:
    spec = architecture_service.update_architecture_by_project(db, project_id, payload)
    return ArchitectureRead.model_validate(spec)
