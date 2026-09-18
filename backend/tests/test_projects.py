"""Tests for Project CRUD (via CRUD layer) and the /projects API endpoints."""
from __future__ import annotations

from app.crud import project as project_crud
from app.schemas.project import ProjectCreate, ProjectUpdate

# ---------------------------------------------------------------------------
# CRUD-layer tests
# ---------------------------------------------------------------------------


def test_crud_create_project(db_session) -> None:
    project = project_crud.create_project(
        db_session, ProjectCreate(name="CRUD Project", description="desc")
    )
    assert project.id is not None
    assert project.name == "CRUD Project"
    assert project.status == "created"


def test_crud_get_project(db_session) -> None:
    created = project_crud.create_project(db_session, ProjectCreate(name="Findable"))
    fetched = project_crud.get_project(db_session, created.id)
    assert fetched is not None
    assert fetched.id == created.id


def test_crud_get_nonexistent_project_returns_none(db_session) -> None:
    assert project_crud.get_project(db_session, "does-not-exist") is None


def test_crud_list_projects(db_session) -> None:
    project_crud.create_project(db_session, ProjectCreate(name="P1"))
    project_crud.create_project(db_session, ProjectCreate(name="P2"))
    results = project_crud.list_projects(db_session)
    assert len(results) == 2


def test_crud_update_project(db_session) -> None:
    project = project_crud.create_project(db_session, ProjectCreate(name="Original"))
    updated = project_crud.update_project(
        db_session, project, ProjectUpdate(name="Updated", status="analyzing")
    )
    assert updated.name == "Updated"
    assert updated.status == "analyzing"


def test_crud_delete_project(db_session) -> None:
    project = project_crud.create_project(db_session, ProjectCreate(name="ToDelete"))
    project_crud.delete_project(db_session, project)
    assert project_crud.get_project(db_session, project.id) is None


# ---------------------------------------------------------------------------
# API-layer tests
# ---------------------------------------------------------------------------


def test_api_create_project(client) -> None:
    response = client.post(
        "/api/v1/projects",
        json={"name": "API Project", "description": "An API-created project"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "API Project"
    assert body["status"] == "created"
    assert "id" in body
    assert "created_at" in body


def test_api_create_project_invalid_input_returns_422(client) -> None:
    # Missing required "name" field.
    response = client.post("/api/v1/projects", json={"description": "no name"})
    assert response.status_code == 422


def test_api_create_project_empty_name_returns_422(client) -> None:
    response = client.post("/api/v1/projects", json={"name": ""})
    assert response.status_code == 422


def test_api_list_projects(client) -> None:
    client.post("/api/v1/projects", json={"name": "Proj A"})
    client.post("/api/v1/projects", json={"name": "Proj B"})

    response = client.get("/api/v1/projects")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert len(body["items"]) == 2


def test_api_get_project_by_id(client) -> None:
    create_response = client.post("/api/v1/projects", json={"name": "Gettable"})
    project_id = create_response.json()["id"]

    response = client.get(f"/api/v1/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["id"] == project_id


def test_api_get_nonexistent_project_returns_404(client) -> None:
    response = client.get("/api/v1/projects/nonexistent-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_api_update_project(client) -> None:
    create_response = client.post("/api/v1/projects", json={"name": "Before Update"})
    project_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/projects/{project_id}",
        json={"name": "After Update", "status": "analyzing"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "After Update"
    assert body["status"] == "analyzing"


def test_api_update_nonexistent_project_returns_404(client) -> None:
    response = client.put(
        "/api/v1/projects/nonexistent-id", json={"name": "Whatever"}
    )
    assert response.status_code == 404


def test_api_delete_project(client) -> None:
    create_response = client.post("/api/v1/projects", json={"name": "To Be Deleted"})
    project_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/projects/{project_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/projects/{project_id}")
    assert get_response.status_code == 404


def test_api_delete_nonexistent_project_returns_404(client) -> None:
    response = client.delete("/api/v1/projects/nonexistent-id")
    assert response.status_code == 404
