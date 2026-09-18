"""Tests for ArchitectureSpec CRUD (via CRUD layer) and API endpoints."""
from __future__ import annotations

from app.crud import architecture as architecture_crud
from app.crud import project as project_crud
from app.schemas.architecture import ArchitectureData, ArchitectureIngest, ArchitectureUpdate
from app.schemas.project import ProjectCreate

# ---------------------------------------------------------------------------
# CRUD-layer tests
# ---------------------------------------------------------------------------


def _make_project(db_session, name: str = "Arch Test Project"):
    return project_crud.create_project(db_session, ProjectCreate(name=name))


def test_crud_create_architecture_spec(db_session) -> None:
    project = _make_project(db_session)
    payload = ArchitectureIngest(
        provider="mock",
        model="mock-v1",
        architecture=ArchitectureData(
            components=["Frontend", "Backend"], routes=[["Frontend", "Backend"]]
        ),
    )
    spec = architecture_crud.create_architecture_spec(db_session, project.id, payload)
    assert spec.project_id == project.id
    assert spec.components == ["Frontend", "Backend"]
    assert spec.routes == [["Frontend", "Backend"]]


def test_crud_get_architecture_spec(db_session) -> None:
    project = _make_project(db_session)
    payload = ArchitectureIngest(architecture=ArchitectureData(components=["A"], routes=[]))
    created = architecture_crud.create_architecture_spec(db_session, project.id, payload)

    fetched = architecture_crud.get_architecture_spec(db_session, created.id)
    assert fetched is not None
    assert fetched.id == created.id


def test_crud_get_architecture_by_project(db_session) -> None:
    project = _make_project(db_session)
    payload = ArchitectureIngest(architecture=ArchitectureData(components=["A"], routes=[]))
    architecture_crud.create_architecture_spec(db_session, project.id, payload)

    fetched = architecture_crud.get_architecture_by_project(db_session, project.id)
    assert fetched is not None
    assert fetched.project_id == project.id


def test_crud_update_architecture_spec(db_session) -> None:
    project = _make_project(db_session)
    payload = ArchitectureIngest(architecture=ArchitectureData(components=["A"], routes=[]))
    spec = architecture_crud.create_architecture_spec(db_session, project.id, payload)

    updated = architecture_crud.update_architecture_spec(
        db_session,
        spec,
        ArchitectureUpdate(
            architecture=ArchitectureData(components=["A", "B"], routes=[["A", "B"]])
        ),
    )
    assert updated.components == ["A", "B"]
    assert updated.routes == [["A", "B"]]


# ---------------------------------------------------------------------------
# API-layer tests
# ---------------------------------------------------------------------------


def _create_project_via_api(client, name: str = "API Arch Project") -> str:
    response = client.post("/api/v1/projects", json={"name": name})
    return response.json()["id"]


def test_api_create_architecture_spec(client) -> None:
    project_id = _create_project_via_api(client)

    response = client.post(
        f"/api/v1/projects/{project_id}/architecture",
        json={
            "provider": "gemini",
            "model": "gemini-2.5-pro",
            "architecture": {
                "components": ["Frontend", "FastAPI", "PostgreSQL"],
                "routes": [["Frontend", "FastAPI"], ["FastAPI", "PostgreSQL"]],
            },
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["project_id"] == project_id
    assert body["components"] == ["Frontend", "FastAPI", "PostgreSQL"]
    assert body["provider"] == "gemini"


def test_api_create_architecture_for_nonexistent_project_returns_404(client) -> None:
    response = client.post(
        "/api/v1/projects/nonexistent-id/architecture",
        json={"architecture": {"components": [], "routes": []}},
    )
    assert response.status_code == 404


def test_api_create_architecture_invalid_data_returns_422(client) -> None:
    project_id = _create_project_via_api(client)
    # "routes" entries must be [source, target] pairs of length 2.
    response = client.post(
        f"/api/v1/projects/{project_id}/architecture",
        json={"architecture": {"components": ["A"], "routes": [["A"]]}},
    )
    assert response.status_code == 422


def test_api_create_duplicate_architecture_returns_409(client) -> None:
    project_id = _create_project_via_api(client)
    body = {"architecture": {"components": ["A"], "routes": []}}
    first = client.post(f"/api/v1/projects/{project_id}/architecture", json=body)
    assert first.status_code == 201

    second = client.post(f"/api/v1/projects/{project_id}/architecture", json=body)
    assert second.status_code == 409


def test_api_get_architecture_by_project(client) -> None:
    project_id = _create_project_via_api(client)
    client.post(
        f"/api/v1/projects/{project_id}/architecture",
        json={"architecture": {"components": ["A", "B"], "routes": [["A", "B"]]}},
    )

    response = client.get(f"/api/v1/projects/{project_id}/architecture")
    assert response.status_code == 200
    assert response.json()["components"] == ["A", "B"]


def test_api_get_architecture_when_none_exists_returns_404(client) -> None:
    project_id = _create_project_via_api(client)
    response = client.get(f"/api/v1/projects/{project_id}/architecture")
    assert response.status_code == 404


def test_api_get_architecture_for_nonexistent_project_returns_404(client) -> None:
    response = client.get("/api/v1/projects/nonexistent-id/architecture")
    assert response.status_code == 404


def test_api_update_architecture(client) -> None:
    project_id = _create_project_via_api(client)
    client.post(
        f"/api/v1/projects/{project_id}/architecture",
        json={"architecture": {"components": ["A"], "routes": []}},
    )

    response = client.put(
        f"/api/v1/projects/{project_id}/architecture",
        json={"architecture": {"components": ["A", "B", "C"], "routes": [["A", "B"]]}},
    )
    assert response.status_code == 200
    assert response.json()["components"] == ["A", "B", "C"]
