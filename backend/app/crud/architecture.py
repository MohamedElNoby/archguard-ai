"""Low-level CRUD operations for the ArchitectureSpec model."""
from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.architecture import ArchitectureSpec
from app.schemas.architecture import ArchitectureIngest, ArchitectureUpdate


def create_architecture_spec(
    db: Session, project_id: str, payload: ArchitectureIngest
) -> ArchitectureSpec:
    spec = ArchitectureSpec(
        project_id=project_id,
        components=payload.architecture.components,
        routes=payload.architecture.routes,
        raw_analysis=payload.raw_analysis,
        provider=payload.provider,
        model=payload.model,
    )
    db.add(spec)
    db.commit()
    db.refresh(spec)
    return spec


def get_architecture_spec(db: Session, spec_id: str) -> Optional[ArchitectureSpec]:
    return db.get(ArchitectureSpec, spec_id)


def get_architecture_by_project(
    db: Session, project_id: str
) -> Optional[ArchitectureSpec]:
    stmt = select(ArchitectureSpec).where(ArchitectureSpec.project_id == project_id)
    return db.execute(stmt).scalar_one_or_none()


def update_architecture_spec(
    db: Session, spec: ArchitectureSpec, payload: ArchitectureUpdate
) -> ArchitectureSpec:
    update_data = payload.model_dump(exclude_unset=True)

    if "architecture" in update_data and update_data["architecture"] is not None:
        arch = update_data.pop("architecture")
        spec.components = arch["components"]
        spec.routes = arch["routes"]

    for field, value in update_data.items():
        setattr(spec, field, value)

    db.add(spec)
    db.commit()
    db.refresh(spec)
    return spec
