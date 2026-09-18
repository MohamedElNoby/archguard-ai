"""Service layer for ArchitectureSpec: HTTP-aware wrapper around CRUD calls."""
from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import architecture as architecture_crud
from app.models.architecture import ArchitectureSpec
from app.schemas.architecture import ArchitectureIngest, ArchitectureUpdate
from app.services.project_service import get_project_or_404


def create_architecture_spec(
    db: Session, project_id: str, payload: ArchitectureIngest
) -> ArchitectureSpec:
    # Ensure the project exists first (404 instead of a raw FK error).
    get_project_or_404(db, project_id)

    existing = architecture_crud.get_architecture_by_project(db, project_id)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Project '{project_id}' already has an ArchitectureSpec. "
                "Use the update endpoint instead."
            ),
        )

    return architecture_crud.create_architecture_spec(db, project_id, payload)


def get_architecture_by_project_or_404(db: Session, project_id: str) -> ArchitectureSpec:
    # Ensure the project itself exists so we can distinguish "project not
    # found" from "project exists but has no architecture spec yet".
    get_project_or_404(db, project_id)

    spec = architecture_crud.get_architecture_by_project(db, project_id)
    if spec is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No ArchitectureSpec found for project '{project_id}'.",
        )
    return spec


def get_architecture_spec_or_404(db: Session, spec_id: str) -> ArchitectureSpec:
    spec = architecture_crud.get_architecture_spec(db, spec_id)
    if spec is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ArchitectureSpec '{spec_id}' not found.",
        )
    return spec


def update_architecture_by_project(
    db: Session, project_id: str, payload: ArchitectureUpdate
) -> ArchitectureSpec:
    spec = get_architecture_by_project_or_404(db, project_id)
    return architecture_crud.update_architecture_spec(db, spec, payload)
