from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.debate import DebateReport
from app.crud.evaluation import (
    create_or_update_defense_evaluation,
    get_defense_evaluation_by_project_id,
)
from app.schemas.evaluation import StudentDefenseRequest, EvaluationResponse
from app.services.evaluation_service import evaluate_student_and_get_solution

router = APIRouter(prefix="/projects", tags=["Defense & Corrected Architecture"])


@router.post(
    "/{project_id}/evaluate",
    response_model=EvaluationResponse,
    summary="Submit student defense, evaluate, persist, and return corrected architecture",
)
def evaluate_defense(
    project_id: str,
    payload: StudentDefenseRequest,
    db: Session = Depends(get_db),
):
    # 1. Verify debate is completed first
    debate_record = (
        db.query(DebateReport)
        .filter(DebateReport.project_id == project_id)
        .first()
    )
    if not debate_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Debate session must be completed first for project '{project_id}'",
        )

    # 2. Compute evaluation and corrected architecture
    result = evaluate_student_and_get_solution(
        project_id=project_id,
        student_defense=payload.student_defense,
        primary_risk=debate_record.primary_risk,
    )

    # 3. Persist into database
    create_or_update_defense_evaluation(
        db=db,
        project_id=project_id,
        student_defense=result["student_defense"],
        student_evaluation=result["student_evaluation"],
        corrected_architecture=result["corrected_architecture"],
        mermaid_diagram=result["mermaid_diagram"],
    )

    return result


@router.get(
    "/{project_id}/evaluation",
    response_model=EvaluationResponse,
    summary="Get saved defense evaluation and corrected architecture from DB",
)
def get_evaluation(
    project_id: str,
    db: Session = Depends(get_db),
):
    record = get_defense_evaluation_by_project_id(db=db, project_id=project_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation record not found for project '{project_id}'",
        )
    return {
        "project_id": record.project_id,
        "student_defense": record.student_defense,
        "student_evaluation": record.student_evaluation,
        "corrected_architecture": record.corrected_architecture,
        "mermaid_diagram": record.mermaid_diagram,
    }


@router.get(
    "/{project_id}/corrected-architecture",
    summary="Get corrected architecture and Mermaid diagram only",
)
def get_corrected_architecture(
    project_id: str,
    db: Session = Depends(get_db),
):
    record = get_defense_evaluation_by_project_id(db=db, project_id=project_id)
    if record:
        return {
            "project_id": record.project_id,
            "corrected_architecture": record.corrected_architecture,
            "mermaid_diagram": record.mermaid_diagram,
        }

    # Fallback to direct calculation if not evaluated yet
    result = evaluate_student_and_get_solution(
        project_id=project_id,
        student_defense="",
        primary_risk={},
    )
    return {
        "project_id": project_id,
        "corrected_architecture": result.get("corrected_architecture"),
        "mermaid_diagram": result.get("mermaid_diagram"),
    }