"""REST endpoints for the RiskAssessment entity.

Like the architecture endpoints, these are the integration point for the
AI/orchestration teammate's risk-analysis agents (CyberSecurity, SRE,
FinOps, ...). They POST results here using the `RiskIngest` contract (see
app/schemas/risk.py).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.risk import RiskAssessmentRead, RiskIngest, RiskUpdate
from app.services import risk_service

router = APIRouter(prefix="/projects/{project_id}/risks", tags=["Risks"])


@router.post(
    "",
    response_model=RiskAssessmentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Store the AI-generated risk assessment for a project",
)
def create_risk_assessment(
    project_id: str, payload: RiskIngest, db: Session = Depends(get_db)
) -> RiskAssessmentRead:
    assessment = risk_service.create_risk_assessment(db, project_id, payload)
    return RiskAssessmentRead.model_validate(assessment)


@router.get(
    "",
    response_model=RiskAssessmentRead,
    summary="Get the risk assessment for a project",
)
def get_risk_assessment(
    project_id: str, db: Session = Depends(get_db)
) -> RiskAssessmentRead:
    assessment = risk_service.get_risks_by_project_or_404(db, project_id)
    return RiskAssessmentRead.model_validate(assessment)


@router.put(
    "",
    response_model=RiskAssessmentRead,
    summary="Update the risk assessment for a project",
)
def update_risk_assessment(
    project_id: str, payload: RiskUpdate, db: Session = Depends(get_db)
) -> RiskAssessmentRead:
    assessment = risk_service.update_risk_assessment_by_project(db, project_id, payload)
    return RiskAssessmentRead.model_validate(assessment)
