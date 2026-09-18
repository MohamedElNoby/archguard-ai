"""Tests for database connection, initialization, and relationships."""
from __future__ import annotations

from sqlalchemy import inspect

from app.core.database import Base
from app.models.architecture import ArchitectureSpec
from app.models.project import Project
from app.models.risk import RiskAssessment
from tests.conftest import engine


def test_database_connection_works() -> None:
    """A raw connection can be opened against the configured engine."""
    with engine.connect() as conn:
        assert conn is not None


def test_all_expected_tables_are_created() -> None:
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    assert {"projects", "architecture_specs", "risk_assessments"}.issubset(tables)


def test_metadata_registers_all_models() -> None:
    table_names = set(Base.metadata.tables.keys())
    assert "projects" in table_names
    assert "architecture_specs" in table_names
    assert "risk_assessments" in table_names


def test_project_architecture_foreign_key(db_session) -> None:
    project = Project(name="FK Test Project")
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    spec = ArchitectureSpec(
        project_id=project.id,
        components=["A", "B"],
        routes=[["A", "B"]],
    )
    db_session.add(spec)
    db_session.commit()
    db_session.refresh(spec)

    assert spec.project_id == project.id


def test_project_risk_foreign_key(db_session) -> None:
    project = Project(name="FK Test Project 2")
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    assessment = RiskAssessment(project_id=project.id, risks=[])
    db_session.add(assessment)
    db_session.commit()
    db_session.refresh(assessment)

    assert assessment.project_id == project.id


def test_project_relationships_are_navigable(db_session) -> None:
    project = Project(name="Relationship Test Project")
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    spec = ArchitectureSpec(project_id=project.id, components=["X"], routes=[])
    assessment = RiskAssessment(project_id=project.id, risks=[])
    db_session.add_all([spec, assessment])
    db_session.commit()

    db_session.refresh(project)
    assert project.architecture_spec is not None
    assert project.architecture_spec.id == spec.id
    assert project.risk_assessment is not None
    assert project.risk_assessment.id == assessment.id
    assert spec.project.id == project.id
    assert assessment.project.id == project.id


def test_deleting_project_cascades_to_children(db_session) -> None:
    project = Project(name="Cascade Test Project")
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    spec = ArchitectureSpec(project_id=project.id, components=[], routes=[])
    assessment = RiskAssessment(project_id=project.id, risks=[])
    db_session.add_all([spec, assessment])
    db_session.commit()

    spec_id, assessment_id = spec.id, assessment.id

    db_session.delete(project)
    db_session.commit()

    assert db_session.get(ArchitectureSpec, spec_id) is None
    assert db_session.get(RiskAssessment, assessment_id) is None
