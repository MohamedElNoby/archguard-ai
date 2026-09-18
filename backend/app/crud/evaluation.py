from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.evaluation import DefenseEvaluation


def create_or_update_defense_evaluation(
    db: Session,
    project_id: str,
    student_defense: str,
    student_evaluation: Dict[str, Any],
    corrected_architecture: Dict[str, Any],
    mermaid_diagram: str,
) -> DefenseEvaluation:
    """Create or update evaluation record for the project."""
    record = (
        db.query(DefenseEvaluation)
        .filter(DefenseEvaluation.project_id == project_id)
        .first()
    )

    if record:
        record.student_defense = student_defense
        record.student_evaluation = student_evaluation
        record.corrected_architecture = corrected_architecture
        record.mermaid_diagram = mermaid_diagram
        db.commit()
        db.refresh(record)
        return record

    record = DefenseEvaluation(
        project_id=project_id,
        student_defense=student_defense,
        student_evaluation=student_evaluation,
        corrected_architecture=corrected_architecture,
        mermaid_diagram=mermaid_diagram,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_defense_evaluation_by_project_id(
    db: Session, project_id: str
) -> Optional[DefenseEvaluation]:
    """Retrieve saved evaluation by project ID."""
    return (
        db.query(DefenseEvaluation)
        .filter(DefenseEvaluation.project_id == project_id)
        .first()
    )