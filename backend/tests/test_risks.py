"""Tests for RiskAssessment CRUD (via CRUD layer) and API endpoints."""
from __future__ import annotations

from app.crud import project as project_crud
from app.crud import risk as risk_crud
from app.schemas.project import ProjectCreate
from app.schemas.risk import RiskIngest, RiskItem, RiskUpdate

SAMPLE_RISK = {
    "title": "Single Point of Failure",
    "category": "SRE",
    "severity": "CRITICAL",
    "description": "The architecture depends on a single backend server.",
    "evidence": "Only one backend instance is present.",
    "recommendation": "Use multiple instances behind a load balancer.",
    "agent": "SRE",
}

# ---------------------------------------------------------------------------
# CRUD-layer tests
# ---------------------------------------------------------------------------


def _make_project(db_session, name: str = "Risk Test Project"):
    return project_crud.create_project(db_session, ProjectCreate(name=name))


def test_crud_create_risk_assessment(db_session) -> None:
    project = _make_project(db_session)
    payload = RiskIngest(provider="mock", risks=[RiskItem(**SAMPLE_RISK)])
    assessment = risk_crud.create_risk_assessment(db_session, project.id, payload)

    assert assessment.project_id == project.id
    assert len(assessment.risks) == 1
    assert assessment.risks[0]["title"] == "Single Point of Failure"


def test_crud_get_risk_assessment(db_session) -> None:
    project = _make_project(db_session)
    created = risk_crud.create_risk_assessment(
        db_session, project.id, RiskIngest(risks=[RiskItem(**SAMPLE_RISK)])
    )
    fetched = risk_crud.get_risk_assessment(db_session, created.id)
    assert fetched is not None
    assert fetched.id == created.id


def test_crud_get_risks_by_project(db_session) -> None:
    project = _make_project(db_session)
    risk_crud.create_risk_assessment(
        db_session, project.id, RiskIngest(risks=[RiskItem(**SAMPLE_RISK)])
    )
    fetched = risk_crud.get_risks_by_project(db_session, project.id)
    assert fetched is not None
    assert fetched.project_id == project.id


def test_crud_update_risk_assessment(db_session) -> None:
    project = _make_project(db_session)
    assessment = risk_crud.create_risk_assessment(
        db_session, project.id, RiskIngest(risks=[RiskItem(**SAMPLE_RISK)])
    )
    new_risk = {**SAMPLE_RISK, "title": "New Risk", "severity": "LOW"}
    updated = risk_crud.update_risk_assessment(
        db_session, assessment, RiskUpdate(risks=[RiskItem(**new_risk)])
    )
    assert len(updated.risks) == 1
    assert updated.risks[0]["title"] == "New Risk"


# ---------------------------------------------------------------------------
# API-layer tests
# ---------------------------------------------------------------------------


def _create_project_via_api(client, name: str = "API Risk Project") -> str:
    response = client.post("/api/v1/projects", json={"name": name})
    return response.json()["id"]


def test_api_create_risk_assessment(client) -> None:
    project_id = _create_project_via_api(client)

    response = client.post(
        f"/api/v1/projects/{project_id}/risks",
        json={"provider": "gemini", "model": "gemini-2.5-pro", "risks": [SAMPLE_RISK]},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["project_id"] == project_id
    assert len(body["risks"]) == 1
    assert body["risks"][0]["severity"] == "CRITICAL"


def test_api_create_risk_for_nonexistent_project_returns_404(client) -> None:
    response = client.post(
        "/api/v1/projects/nonexistent-id/risks", json={"risks": [SAMPLE_RISK]}
    )
    assert response.status_code == 404


def test_api_create_risk_invalid_severity_returns_422(client) -> None:
    project_id = _create_project_via_api(client)
    bad_risk = {**SAMPLE_RISK, "severity": "NOT_A_REAL_SEVERITY"}
    response = client.post(
        f"/api/v1/projects/{project_id}/risks", json={"risks": [bad_risk]}
    )
    assert response.status_code == 422


def test_api_create_risk_missing_required_field_returns_422(client) -> None:
    project_id = _create_project_via_api(client)
    bad_risk = {k: v for k, v in SAMPLE_RISK.items() if k != "title"}
    response = client.post(
        f"/api/v1/projects/{project_id}/risks", json={"risks": [bad_risk]}
    )
    assert response.status_code == 422


def test_api_create_duplicate_risk_assessment_returns_409(client) -> None:
    project_id = _create_project_via_api(client)
    body = {"risks": [SAMPLE_RISK]}
    first = client.post(f"/api/v1/projects/{project_id}/risks", json=body)
    assert first.status_code == 201

    second = client.post(f"/api/v1/projects/{project_id}/risks", json=body)
    assert second.status_code == 409


def test_api_get_risks_by_project(client) -> None:
    project_id = _create_project_via_api(client)
    client.post(f"/api/v1/projects/{project_id}/risks", json={"risks": [SAMPLE_RISK]})

    response = client.get(f"/api/v1/projects/{project_id}/risks")
    assert response.status_code == 200
    assert len(response.json()["risks"]) == 1


def test_api_get_risks_when_none_exist_returns_404(client) -> None:
    project_id = _create_project_via_api(client)
    response = client.get(f"/api/v1/projects/{project_id}/risks")
    assert response.status_code == 404


def test_api_get_risks_for_nonexistent_project_returns_404(client) -> None:
    response = client.get("/api/v1/projects/nonexistent-id/risks")
    assert response.status_code == 404


def test_api_update_risk_assessment(client) -> None:
    project_id = _create_project_via_api(client)
    client.post(f"/api/v1/projects/{project_id}/risks", json={"risks": [SAMPLE_RISK]})

    new_risk = {**SAMPLE_RISK, "title": "Updated Risk"}
    response = client.put(
        f"/api/v1/projects/{project_id}/risks", json={"risks": [new_risk]}
    )
    assert response.status_code == 200
    assert response.json()["risks"][0]["title"] == "Updated Risk"
