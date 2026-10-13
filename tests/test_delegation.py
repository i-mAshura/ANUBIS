import pytest
from anubis.services.auth.service import token_service


@pytest.fixture
def agent_hierarchy(client):
    """
    Registers an owner and a 3-tier agent hierarchy:
    Planner (Parent) -> Researcher (Sub-agent) -> Writer (Sub-sub-agent)
    """
    owner_resp = client.post("/owners", json={"name": "Engineering Lead", "email": "eng_lead@corp.local"})
    owner_id = owner_resp.json()["id"]

    # 1. Planner
    p_resp = client.post("/agents", json={"name": "Planner-Agent", "owner_id": owner_id, "purpose": "Task orchestration", "risk_tier": "medium"})
    planner_id = p_resp.json()["agent"]["id"]

    # 2. Researcher
    r_resp = client.post("/agents", json={"name": "Researcher-Agent", "owner_id": owner_id, "purpose": "Data discovery", "risk_tier": "low"})
    researcher_id = r_resp.json()["agent"]["id"]

    # 3. Writer
    w_resp = client.post("/agents", json={"name": "Writer-Agent", "owner_id": owner_id, "purpose": "Report generation", "risk_tier": "low"})
    writer_id = w_resp.json()["agent"]["id"]

    # 4. Register tools
    client.post("/tools", json={"name": "read_data", "server": "records", "required_scope": "tools:read"})

    return {
        "owner_id": owner_id,
        "planner_id": planner_id,
        "researcher_id": researcher_id,
        "writer_id": writer_id
    }


def test_task_creation_and_lifecycle(client, agent_hierarchy):
    planner_id = agent_hierarchy["planner_id"]

    # Create task
    task_resp = client.post("/tasks", json={
        "root_agent_id": planner_id,
        "on_behalf_of": "ciso@corp.local",
        "intent": "Compile enterprise security audit report",
        "requested_scope": ["tools:read", "tools:search"]
    })
    assert task_resp.status_code == 201
    task_data = task_resp.json()
    assert task_data["status"] == "running"
    assert task_data["on_behalf_of"] == "ciso@corp.local"
    assert task_data["id"].startswith("task_")

    task_id = task_data["id"]

    # Query task
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["intent"] == "Compile enterprise security audit report"

    # Complete task
    patch_resp = client.patch(f"/tasks/{task_id}", json={"status": "completed"})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["status"] == "completed"
    assert patch_resp.json()["completed_at"] is not None


def test_token_exchange_scope_narrowing_and_act_chain(client, agent_hierarchy):
    planner_id = agent_hierarchy["planner_id"]
    researcher_id = agent_hierarchy["researcher_id"]

    # Issue root token to Planner
    issued_planner = token_service.issue_token(
        agent_id=planner_id,
        instance_id="inst-planner-1",
        scope=["tools:read", "tools:search", "tools:write"],
        task_id="task-q3-audit",
        on_behalf_of="director@corp.local"
    )
    planner_token = issued_planner["access_token"]
    planner_jti = issued_planner["jti"]

    # Planner exchanges token for Researcher with narrowed scope
    exchange_resp = client.post(
        "/auth/exchange",
        headers={"Authorization": f"Bearer {planner_token}"},
        json={
            "child_agent_id": researcher_id,
            "child_instance_id": "inst-researcher-1",
            "requested_scope": ["tools:read", "tools:search"]
        }
    )
    assert exchange_resp.status_code == 200
    res_data = exchange_resp.json()
    claims = res_data["claims"]

    assert claims["sub"] == researcher_id
    assert claims["parent_jti"] == planner_jti
    assert claims["on_behalf_of"] == "director@corp.local"
    assert set(claims["scope"]) == {"tools:read", "tools:search"}
    # Cryptographic act lineage claim extended: [Planner, Researcher]
    assert claims["act"] == [planner_id, researcher_id]


def test_privilege_escalation_attempt_strictly_denied(client, agent_hierarchy):
    planner_id = agent_hierarchy["planner_id"]
    researcher_id = agent_hierarchy["researcher_id"]

    # Issue token to Planner with limited scopes: only read and search
    issued_planner = token_service.issue_token(
        agent_id=planner_id,
        instance_id="inst-p",
        scope=["tools:read", "tools:search"]
    )
    planner_token = issued_planner["access_token"]

    # Sub-agent attempts privilege escalation by requesting 'tools:admin' and 'tools:write'
    escalate_resp = client.post(
        "/auth/exchange",
        headers={"Authorization": f"Bearer {planner_token}"},
        json={
            "child_agent_id": researcher_id,
            "requested_scope": ["tools:read", "tools:admin", "tools:write"]
        }
    )
    assert escalate_resp.status_code == 403
    err_detail = escalate_resp.json()["detail"].lower()
    assert "privilege escalation attempt" in err_detail
    assert "tools:admin" in err_detail


def test_multi_agent_workflow_simulation(client, agent_hierarchy):
    """
    Simulates complete delegation pipeline:
    Planner -> Researcher -> Writer -> Gateway execution -> Audit trail attribution
    """
    planner_id = agent_hierarchy["planner_id"]
    researcher_id = agent_hierarchy["researcher_id"]
    writer_id = agent_hierarchy["writer_id"]

    # 1. Task initialization
    task_resp = client.post("/tasks", json={
        "root_agent_id": planner_id,
        "on_behalf_of": "chief_risk_officer@corp.local",
        "intent": "Global Threat Surface Analysis",
        "requested_scope": ["tools:read", "tools:search", "tools:write"]
    })
    task_id = task_resp.json()["id"]

    # 2. Planner token
    root_token = token_service.issue_token(
        agent_id=planner_id,
        instance_id="inst-plan",
        scope=["tools:read", "tools:search", "tools:write"],
        task_id=task_id,
        on_behalf_of="chief_risk_officer@corp.local"
    )["access_token"]

    # 3. Delegation 1: Planner -> Researcher (narrow to: read, search)
    resp_delegation_1 = client.post(
        "/auth/exchange",
        headers={"Authorization": f"Bearer {root_token}"},
        json={
            "child_agent_id": researcher_id,
            "requested_scope": ["tools:read", "tools:search"]
        }
    )
    assert resp_delegation_1.status_code == 200
    researcher_token = resp_delegation_1.json()["access_token"]

    # 4. Delegation 2: Researcher -> Writer (narrow to: read only)
    resp_delegation_2 = client.post(
        "/auth/exchange",
        headers={"Authorization": f"Bearer {researcher_token}"},
        json={
            "child_agent_id": writer_id,
            "requested_scope": ["tools:read"]
        }
    )
    assert resp_delegation_2.status_code == 200
    writer_token = resp_delegation_2.json()["access_token"]
    writer_claims = resp_delegation_2.json()["claims"]

    # Lineage is now 3 tiers deep
    expected_lineage = [planner_id, researcher_id, writer_id]
    assert writer_claims["act"] == expected_lineage
    assert writer_claims["scope"] == ["tools:read"]

    # 5. Writer executes tool call through Gateway
    gw_resp = client.post(
        "/mcp/records",
        headers={"Authorization": f"Bearer {writer_token}"},
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "read_data", "arguments": {}}
        }
    )
    assert gw_resp.status_code == 200
    assert gw_resp.json()["result"]["status"] == "success"

    # 6. Audit Trail verification of delegation attribution
    audit_resp = client.get(f"/audit?agent_id={writer_id}")
    assert audit_resp.status_code == 200
    records = audit_resp.json()
    assert len(records) >= 1
    # Check that audit record captured the entire multi-agent act chain!
    assert records[0]["chain"] == expected_lineage


def test_cannot_delegate_to_revoked_or_suspended_agent(client, agent_hierarchy):
    planner_id = agent_hierarchy["planner_id"]
    researcher_id = agent_hierarchy["researcher_id"]

    root_token = token_service.issue_token(
        agent_id=planner_id,
        instance_id="inst-plan",
        scope=["tools:read"]
    )["access_token"]

    # Suspend researcher
    client.patch(f"/agents/{researcher_id}", json={"status": "suspended"})

    # Attempt to delegate
    resp = client.post(
        "/auth/exchange",
        headers={"Authorization": f"Bearer {root_token}"},
        json={
            "child_agent_id": researcher_id,
            "requested_scope": ["tools:read"]
        }
    )
    assert resp.status_code == 403
    assert "suspended" in resp.json()["detail"].lower()
