"""Service layer for RiskAssessment: HTTP-aware wrapper around CRUD calls."""
from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import risk as risk_crud
from app.models.risk import RiskAssessment
from app.schemas.risk import RiskIngest, RiskUpdate
from app.services.project_service import get_project_or_404


def create_risk_assessment(
    db: Session, project_id: str, payload: RiskIngest
) -> RiskAssessment:
    get_project_or_404(db, project_id)

    existing = risk_crud.get_risks_by_project(db, project_id)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Project '{project_id}' already has a RiskAssessment. "
                "Use the update endpoint instead."
            ),
        )

    return risk_crud.create_risk_assessment(db, project_id, payload)


def get_risks_by_project_or_404(db: Session, project_id: str) -> RiskAssessment:
    get_project_or_404(db, project_id)

    assessment = risk_crud.get_risks_by_project(db, project_id)
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No RiskAssessment found for project '{project_id}'.",
        )
    return assessment


def get_risk_assessment_or_404(db: Session, assessment_id: str) -> RiskAssessment:
    assessment = risk_crud.get_risk_assessment(db, assessment_id)
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RiskAssessment '{assessment_id}' not found.",
        )
    return assessment


def update_risk_assessment_by_project(
    db: Session, project_id: str, payload: RiskUpdate
) -> RiskAssessment:
    assessment = get_risks_by_project_or_404(db, project_id)
    return risk_crud.update_risk_assessment(db, assessment, payload)
