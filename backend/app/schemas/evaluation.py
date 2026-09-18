from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class StudentDefenseRequest(BaseModel):
    student_defense: str


class StudentEvaluation(BaseModel):
    overall_score: float
    criteria: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    missing_considerations: List[str]
    improvement_recommendations: List[str]
    evaluation_summary: str


class EvaluationResponse(BaseModel):
    project_id: str
    student_defense: str
    student_evaluation: StudentEvaluation
    corrected_architecture: Dict[str, Any]
    mermaid_diagram: str