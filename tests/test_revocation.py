import pytest
from anubis.services.auth.service import token_service
from anubis.services.revocation.service import RevocationService


@pytest.fixture
def active_agent_and_tokens(client):
    owner_resp = client.post("/owners", json={"name": "KillSwitch Lead", "email": "ks_lead@corp.local"})
    owner_id = owner_resp.json()["id"]

    agent_resp = client.post("/agents", json={
        "name": "Target-KS-Agent",
        "owner_id": owner_id,
        "purpose": "Verify multi-dimensional kill switches"
    })
    agent_id = agent_resp.json()["agent"]["id"]

    client.post("/tools", json={"name": "read_metrics", "server": "ops", "required_scope": "tools:read"})

    # Issue token for instance 1
    issued_1 = token_service.issue_token(
        agent_id=agent_id,
        instance_id="inst-alpha",
        scope=["tools:read"],
        task_id="task-recon-01",
        on_behalf_of="sec_operator@corp.local"
    )
    # Issue token for instance 2
    issued_2 = token_service.issue_token(
        agent_id=agent_id,
        instance_id="inst-beta",
        scope=["tools:read"],
        task_id="task-recon-02",
        on_behalf_of="sec_operator@corp.local"
    )

    return {
        "agent_id": agent_id,
        "token_inst1": issued_1["access_token"],
        "jti_inst1": issued_1["jti"],
        "token_inst2": issued_2["access_token"],
        "jti_inst2": issued_2["jti"]
    }


def test_kill_switch_by_agent_id(client, active_agent_and_tokens):
    agent_id = active_agent_and_tokens["agent_id"]
    token = active_agent_and_tokens["token_inst1"]

    # Call succeeds before revocation
    resp_before = client.post(
        "/mcp/ops",
        headers={"Authorization": f"Bearer {token}"},
        json={"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "read_metrics", "arguments": {}}}
    )
    assert resp_before.status_code == 200

    # Trigger kill switch for the whole agent
    rev_resp = client.post("/revocations", json={
        "target_type": "agent",
        "target_id": agent_id,
        "reason": "Suspected compromise during external audit"
    })
    assert rev_resp.status_code == 201

    # Call MUST be blocked immediately with 403
    resp_after = client.post(
        "/mcp/ops",
        headers={"Authorization": f"Bearer {token}"},
        json={"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "read_metrics", "arguments": {}}}
    )
    assert resp_after.status_code == 403
    assert "kill switch" in resp_after.json()["detail"].lower()


def test_kill_switch_by_instance_id(client, active_agent_and_tokens):
    token_inst1 = active_agent_and_tokens["token_inst1"]  # inst-alpha
    token_inst2 = active_agent_and_tokens["token_inst2"]  # inst-beta

    # Revoke only instance 'inst-alpha'
    client.post("/revocations", json={
        "target_type": "instance",
        "target_id": "inst-alpha",
        "reason": "Host node compromised"
    })

    # inst-alpha MUST be blocked
    resp_alpha = client.post(
        "/mcp/ops",
        headers={"Authorization": f"Bearer {token_inst1}"},
        json={"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "read_metrics", "arguments": {}}}
    )
    assert resp_alpha.status_code == 403
    assert "instance 'inst-alpha' has been terminated" in resp_alpha.json()["detail"].lower()

    # inst-beta MUST continue working unaffected
    resp_beta = client.post(
        "/mcp/ops",
        headers={"Authorization": f"Bearer {token_inst2}"},
        json={"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "read_metrics", "arguments": {}}}
    )
    assert resp_beta.status_code == 200


def test_kill_switch_by_token_jti(client, active_agent_and_tokens):
    token_inst1 = active_agent_and_tokens["token_inst1"]
    jti_inst1 = active_agent_and_tokens["jti_inst1"]

    # Revoke specific stolen token JTI
    client.post("/revocations", json={
        "target_type": "token",
        "target_id": jti_inst1,
        "reason": "Token leaked in client log"
    })

    resp = client.post(
        "/mcp/ops",
        headers={"Authorization": f"Bearer {token_inst1}"},
        json={"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "read_metrics", "arguments": {}}}
    )
    assert resp.status_code == 403
    assert "blacklisted" in resp.json()["detail"].lower()


def test_kill_switch_by_human_principal(client, active_agent_and_tokens):
    token = active_agent_and_tokens["token_inst1"]  # on_behalf_of: sec_operator@corp.local

    # Revoke all agents acting on behalf of departed human operator
    client.post("/revocations", json={
        "target_type": "principal",
        "target_id": "sec_operator@corp.local",
        "reason": "Employee offboarded immediately"
    })

    resp = client.post(
        "/mcp/ops",
        headers={"Authorization": f"Bearer {token}"},
        json={"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "read_metrics", "arguments": {}}}
    )
    assert resp.status_code == 403
    assert "suspended" in resp.json()["detail"].lower()
