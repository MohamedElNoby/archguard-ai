"""Project ORM model.

A Project is the top-level entity representing one submitted architecture
review (e.g. "Smart Hospital Management System"). It owns exactly one
ArchitectureSpec, one RiskAssessment, and one DebateReport (1-to-1 relationships),
which is the most practical design for a hackathon MVP: each upload/analysis run
produces one structured spec, one risk report, and one multi-agent debate report.
"""
from __future__ import annotations

import datetime as dt
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:  # pragma: no cover - only used for static type checking
    from app.models.architecture import ArchitectureSpec
    from app.models.risk import RiskAssessment
    from app.models.debate import DebateReport
    from app.models.evaluation import DefenseEvaluation


def _uuid() -> str:
    return str(uuid.uuid4())


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_uuid, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Path to the uploaded architecture diagram / ERD image. This column is
    # written to by the teammate's upload endpoint; it is nullable
    # because a Project may be created before an image is uploaded, or
    # created directly via mock data with no image at all.
    diagram_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Free-form status field useful for the frontend to show progress, e.g.
    # "created" -> "analyzing" -> "completed". Not enforced as an enum at
    # the DB level to keep the hackathon schema flexible.
    status: Mapped[str] = mapped_column(String(50), default="created", nullable=False)

    created_at: Mapped[dt.datetime] = mapped_column(
        default=lambda: dt.datetime.now(dt.timezone.utc), nullable=False
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        default=lambda: dt.datetime.now(dt.timezone.utc),
        onupdate=lambda: dt.datetime.now(dt.timezone.utc),
        nullable=False,
    )

    # --- Relationships ---------------------------------------------------
    architecture_spec: Mapped[Optional["ArchitectureSpec"]] = relationship(
        "ArchitectureSpec",
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    risk_assessment: Mapped[Optional["RiskAssessment"]] = relationship(
        "RiskAssessment",
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    debate_report: Mapped[Optional["DebateReport"]] = relationship(
        "DebateReport",
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    defense_evaluation: Mapped[Optional["DefenseEvaluation"]] = relationship(
    "DefenseEvaluation",
    back_populates="project",
    uselist=False,
    cascade="all, delete-orphan",
    passive_deletes=True,
)

    def __repr__(self) -> str:  # pragma: no cover - debugging aid only
        return f"<Project id={self.id!r} name={self.name!r} status={self.status!r}>"