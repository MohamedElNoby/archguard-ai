"""Low-level CRUD operations for the RiskAssessment model."""
from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.risk import RiskAssessment
from app.schemas.risk import RiskIngest, RiskUpdate


def _risks_to_dicts(risks) -> list[dict]:
    """Convert a list of RiskItem (or dicts) into plain JSON-serializable dicts."""
    result = []
    for r in risks:
        if hasattr(r, "model_dump"):
            result.append(r.model_dump(mode="json"))
        else:
            result.append(r)
    return result


def create_risk_assessment(
    db: Session, project_id: str, payload: RiskIngest
) -> RiskAssessment:
    assessment = RiskAssessment(
        project_id=project_id,
        risks=_risks_to_dicts(payload.risks),
        raw_analysis=payload.raw_analysis,
        provider=payload.provider,
        model=payload.model,
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment


def get_risk_assessment(db: Session, assessment_id: str) -> Optional[RiskAssessment]:
    return db.get(RiskAssessment, assessment_id)


def get_risks_by_project(
    db: Session, project_id: str
) -> Optional[RiskAssessment]:
    stmt = select(RiskAssessment).where(RiskAssessment.project_id == project_id)
    return db.execute(stmt).scalar_one_or_none()


def update_risk_assessment(
    db: Session, assessment: RiskAssessment, payload: RiskUpdate
) -> RiskAssessment:
    update_data = payload.model_dump(exclude_unset=True)

    if "risks" in update_data and update_data["risks"] is not None:
        assessment.risks = update_data.pop("risks")

    for field, value in update_data.items():
        setattr(assessment, field, value)

    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment
