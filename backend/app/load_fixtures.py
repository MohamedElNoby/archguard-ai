"""
Mock data loader.

Loads the JSON fixtures in app/fixtures/ into the configured database so the
frontend team can build against realistic data before the real Gemini
integration is finished.

Usage (from the `backend/` directory, with the venv activated):

    python -m app.load_fixtures

Re-running this script is safe: it clears existing Project /
ArchitectureSpec / RiskAssessment rows first, then reloads the fixtures
fresh (idempotent for demo purposes).
"""
from __future__ import annotations

import json
from pathlib import Path

from app.core.database import Base, SessionLocal, engine, init_db
from app.crud.architecture import create_architecture_spec
from app.crud.project import create_project
from app.crud.risk import create_risk_assessment
from app.models.architecture import ArchitectureSpec
from app.models.project import Project
from app.models.risk import RiskAssessment
from app.schemas.architecture import ArchitectureIngest
from app.schemas.project import ProjectCreate
from app.schemas.risk import RiskIngest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _load_json(filename: str) -> list[dict]:
    path = FIXTURES_DIR / filename
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def clear_existing_data() -> None:
    """Remove all existing rows (children first to respect foreign keys)."""
    with SessionLocal() as db:
        db.query(RiskAssessment).delete()
        db.query(ArchitectureSpec).delete()
        db.query(Project).delete()
        db.commit()


def load_fixtures() -> None:
    # Make sure tables exist before we touch them.
    init_db()
    clear_existing_data()

    projects_data = _load_json("projects.json")
    architectures_data = _load_json("architectures.json")
    risks_data = _load_json("risks.json")

    with SessionLocal() as db:
        name_to_id: dict[str, str] = {}

        for entry in projects_data:
            payload = ProjectCreate(
                name=entry["name"],
                description=entry.get("description"),
                diagram_path=entry.get("diagram_path"),
            )
            project = create_project(db, payload)
            project.status = entry.get("status", project.status)
            db.add(project)
            db.commit()
            name_to_id[entry["name"]] = project.id
            print(f"  created project: {project.name!r} (id={project.id})")

        for entry in architectures_data:
            project_name = entry["project_name"]
            project_id = name_to_id.get(project_name)
            if project_id is None:
                print(f"  ! skipping architecture for unknown project {project_name!r}")
                continue
            payload = ArchitectureIngest(
                provider=entry.get("provider"),
                model=entry.get("model"),
                architecture=entry["architecture"],
                raw_analysis=entry.get("raw_analysis"),
            )
            create_architecture_spec(db, project_id, payload)
            print(f"  created architecture spec for: {project_name!r}")

        for entry in risks_data:
            project_name = entry["project_name"]
            project_id = name_to_id.get(project_name)
            if project_id is None:
                print(f"  ! skipping risks for unknown project {project_name!r}")
                continue
            payload = RiskIngest(
                provider=entry.get("provider"),
                model=entry.get("model"),
                risks=entry["risks"],
                raw_analysis=entry.get("raw_analysis"),
            )
            create_risk_assessment(db, project_id, payload)
            print(f"  created risk assessment for: {project_name!r} "
                  f"({len(entry['risks'])} risks)")

    print("\nMock data loaded successfully.")


if __name__ == "__main__":
    print(f"Loading fixtures into database (Base metadata tables: "
          f"{list(Base.metadata.tables.keys())}) ...")
    load_fixtures()
