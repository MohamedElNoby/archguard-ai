from typing import Optional
from sqlalchemy.orm import Session
from app.models.debate import DebateReport
from app.schemas.debate import DebateReportCreate


def create_or_update_debate_report(
    db: Session, project_id: str, payload: DebateReportCreate
) -> DebateReport:
    """Creates a new debate report or updates existing one for the project."""
    existing = db.query(DebateReport).filter(DebateReport.project_id == project_id).first()
    
    if existing:
        existing.primary_risk = payload.primary_risk
        existing.agents = payload.agents
        existing.debate_summary = payload.debate_summary
        db.commit()
        db.refresh(existing)
        return existing

    db_item = DebateReport(
        project_id=project_id,
        primary_risk=payload.primary_risk,
        agents=payload.agents,
        debate_summary=payload.debate_summary
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_debate_report_by_project_id(db: Session, project_id: str) -> Optional[DebateReport]:
    """Retrieve debate report for a specific project."""
    return db.query(DebateReport).filter(DebateReport.project_id == project_id).first()