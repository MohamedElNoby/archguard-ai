"""RiskAssessment ORM model.

Stores the risk-analysis output produced by the AI red-team agents
(CyberSecurity, SRE/Scalability, Cloud/FinOps, ...).

Design decision: a single RiskAssessment row per project holds the *entire*
list of risks as a JSON array (see `risks` column), rather than a separate
`Risk` table with one row per risk. This is the practical hackathon choice
because:

  1. Risks are always read/written together as one full report per project.
  2. It keeps writes atomic (one INSERT/UPDATE per AI run) and matches the
     `{"risks": [...]}` shape the AI layer already produces.
  3. It avoids extra JOINs on the hot "get risks for project" read path.

Each entry inside the `risks` JSON array is expected to have the shape:
{
    "title": str,
    "category": str,       # e.g. "CyberSecurity", "SRE", "FinOps"
    "severity": str,       # e.g. "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
    "description": str,
    "evidence": str,
    "recommendation": str,
    "agent": str           # which AI agent produced this risk
}
This shape is validated at the API boundary by Pydantic schemas
(see app/schemas/risk.py), not enforced by the database itself, so new
optional fields can be added by the AI team without a migration.
"""
from __future__ import annotations

import datetime as dt
import uuid
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:  # pragma: no cover
    from app.models.project import Project


def _uuid() -> str:
    return str(uuid.uuid4())


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_uuid, index=True
    )

    # One project -> one risk assessment report (1-to-1, enforced by unique).
    project_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # List of risk dicts - see module docstring for expected shape.
    risks: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)

    # Full raw AI payload, kept for auditability (same rationale as
    # ArchitectureSpec.raw_analysis).
    raw_analysis: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON, nullable=True
    )

    provider: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)

    created_at: Mapped[dt.datetime] = mapped_column(
        default=lambda: dt.datetime.now(dt.timezone.utc), nullable=False
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        default=lambda: dt.datetime.now(dt.timezone.utc),
        onupdate=lambda: dt.datetime.now(dt.timezone.utc),
        nullable=False,
    )

    # --- Relationships ---------------------------------------------------
    project: Mapped["Project"] = relationship(
        "Project", back_populates="risk_assessment"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<RiskAssessment id={self.id!r} project_id={self.project_id!r} "
            f"risks={len(self.risks)}>"
        )
