"""Import all ORM models here so that Base.metadata is fully populated
and relationship() string references resolve correctly, no matter which
module triggers the import first.
"""
from app.models.project import Project
from app.models.architecture import ArchitectureSpec
from app.models.risk import RiskAssessment
from app.models.debate import DebateReport
from app.models.evaluation import DefenseEvaluation

__all__ = [
    "Project",
    "ArchitectureSpec",
    "RiskAssessment",
    "DebateReport",
    "DefenseEvaluation",
]