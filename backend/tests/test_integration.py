"""
Full end-to-end integration test, driven purely through the HTTP API
(exactly as the frontend / AI teammate would use it):

  1. Create a Project.
  2. Save an ArchitectureSpec for it.
  3. Save a RiskAssessment for it.
  4. Retrieve the Project.
  5. Retrieve its ArchitectureSpec.
  6. Retrieve its RiskAssessment.
  7. Verify all relationships (foreign keys line up).
  8. Verify the stored values match exactly what was submitted.
"""
from __future__ import annotations


def test_full_project_lifecycle_end_to_end(client) -> None:
    # 1. Create a Project.
    project_payload = {
        "name": "Integration Test Project",
        "description": "End-to-end test project",
        "diagram_path": "uploads/integration-test.png",
    }
    create_project_resp = client.post("/api/v1/projects", json=project_payload)
    assert create_project_resp.status_code == 201
    project = create_project_resp.json()
    project_id = project["id"]
    assert project["name"] == project_payload["name"]
    assert project["description"] == project_payload["description"]
    assert project["diagram_path"] == project_payload["diagram_path"]

    # 2. Save an ArchitectureSpec (simulating the AI teammate's Gemini output).
    architecture_payload = {
        "provider": "gemini",
        "model": "gemini-2.5-pro",
        "architecture": {
            "components": ["Frontend", "FastAPI", "PostgreSQL", "Redis"],
            "routes": [
                ["Frontend", "FastAPI"],
                ["FastAPI", "PostgreSQL"],
                ["FastAPI", "Redis"],
            ],
        },
        "raw_analysis": {"confidence": 0.92},
    }
    create_arch_resp = client.post(
        f"/api/v1/projects/{project_id}/architecture", json=architecture_payload
    )
    assert create_arch_resp.status_code == 201
    architecture = create_arch_resp.json()
    assert architecture["project_id"] == project_id

    # 3. Save a RiskAssessment (simulating the AI red-team agents' output).
    risk_payload = {
        "provider": "gemini",
        "model": "gemini-2.5-pro",
        "risks": [
            {
                "title": "Single Point of Failure",
                "category": "SRE",
                "severity": "CRITICAL",
                "description": "The architecture depends on a single backend server.",
                "evidence": "Only one backend instance is present.",
                "recommendation": "Use multiple instances behind a load balancer.",
                "agent": "SRE",
            },
            {
                "title": "No Rate Limiting",
                "category": "CyberSecurity",
                "severity": "HIGH",
                "description": "Public endpoints have no rate limiting.",
                "evidence": "No gateway-level throttling configured.",
                "recommendation": "Add rate limiting at the API Gateway.",
                "agent": "CyberSecurity",
            },
        ],
    }
    create_risk_resp = client.post(
        f"/api/v1/projects/{project_id}/risks", json=risk_payload
    )
    assert create_risk_resp.status_code == 201
    risk_assessment = create_risk_resp.json()
    assert risk_assessment["project_id"] == project_id

    # 4. Retrieve the Project.
    get_project_resp = client.get(f"/api/v1/projects/{project_id}")
    assert get_project_resp.status_code == 200
    fetched_project = get_project_resp.json()
    assert fetched_project["id"] == project_id
    assert fetched_project["name"] == project_payload["name"]

    # 5. Retrieve its ArchitectureSpec.
    get_arch_resp = client.get(f"/api/v1/projects/{project_id}/architecture")
    assert get_arch_resp.status_code == 200
    fetched_architecture = get_arch_resp.json()

    # 6. Retrieve its RiskAssessment.
    get_risk_resp = client.get(f"/api/v1/projects/{project_id}/risks")
    assert get_risk_resp.status_code == 200
    fetched_risks = get_risk_resp.json()

    # 7. Verify all relationships: both child records point back at the
    # same project_id, and that project_id matches the created project.
    assert fetched_architecture["project_id"] == fetched_project["id"]
    assert fetched_risks["project_id"] == fetched_project["id"]

    # 8. Verify stored values match exactly what was submitted.
    assert fetched_architecture["components"] == architecture_payload["architecture"]["components"]
    assert fetched_architecture["routes"] == architecture_payload["architecture"]["routes"]
    assert fetched_architecture["provider"] == architecture_payload["provider"]
    assert fetched_architecture["model"] == architecture_payload["model"]
    assert fetched_architecture["raw_analysis"] == architecture_payload["raw_analysis"]

    assert len(fetched_risks["risks"]) == 2
    titles = {r["title"] for r in fetched_risks["risks"]}
    assert titles == {"Single Point of Failure", "No Rate Limiting"}
    severities = {r["severity"] for r in fetched_risks["risks"]}
    assert severities == {"CRITICAL", "HIGH"}

    # Bonus: deleting the project cascades to its children.
    delete_resp = client.delete(f"/api/v1/projects/{project_id}")
    assert delete_resp.status_code == 204

    assert client.get(f"/api/v1/projects/{project_id}").status_code == 404
    assert client.get(f"/api/v1/projects/{project_id}/architecture").status_code == 404
    assert client.get(f"/api/v1/projects/{project_id}/risks").status_code == 404
