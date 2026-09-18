"""ArchitectureSpec ORM model.

Stores the structured architecture representation extracted/analyzed by the
AI layer (owned by the "Backend Core & Orchestration" teammate). This table
is intentionally provider-agnostic: it does not know or care whether the
data came from Gemini, Claude, OpenAI, or a mock fixture.

Design decision: `components` and `routes` are stored as JSON columns
(SQLite's JSON type, which is stored as TEXT but transparently
serialized/deserialized by SQLAlchemy) rather than normalized into separate
tables. This is the practical choice for a 6-day hackathon: the AI output
shape is still evolving, and JSON storage means the database layer does not
need to change every time the AI teammate tweaks its output format.
`raw_analysis` retains the complete original AI JSON payload for
auditability/debugging, independent of how `components`/`routes` are
projected out of it.
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


class ArchitectureSpec(Base):
    __tablename__ = "architecture_specs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_uuid, index=True
    )

    # One project -> one architecture spec. `unique=True` enforces the
    # 1-to-1 relationship at the database level.
    project_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # Structured architecture data, e.g.:
    # ["Frontend", "FastAPI", "PostgreSQL", "Redis"]
    components: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)

    # e.g. [["Frontend", "FastAPI"], ["FastAPI", "PostgreSQL"]]
    routes: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)

    # Full, untouched AI response payload for auditing/debugging purposes.
    raw_analysis: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON, nullable=True
    )

    # Metadata about which AI provider/model produced this spec. Kept as
    # plain strings (not an enum/FK) so new providers require zero schema
    # changes.
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
        "Project", back_populates="architecture_spec"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<ArchitectureSpec id={self.id!r} project_id={self.project_id!r} "
            f"components={len(self.components)}>"
        )
