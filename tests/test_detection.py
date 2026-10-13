import pytest
from anubis.services.auth.service import token_service


def setup_agent_and_token(client, scope=None):
    if scope is None:
        scope = ["tools:read", "tools:email"]
    owner_res = client.post("/owners", json={"name": "Security Team", "email": "sec@underworld.corp"})
    owner_id = owner_res.json()["id"]

    reg_res = client.post("/agents", json={
        "name": "Sentinel-AI",
        "owner_id": owner_id,
        "purpose": "Anomaly detection test agent",
        "risk_tier": "low"
    })
    agent_id = reg_res.json()["agent"]["id"]

    issued = token_service.issue_token(
        agent_id=agent_id,
        instance_id="inst-sec-1",
        scope=scope,
        task_id="task-detection-test",
        on_behalf_of="sec_admin",
        ttl_minutes=15
    )
    token = issued["access_token"]
    return agent_id, token


def test_baseline_tracking_and_retrieval(client):
    agent_id, token = setup_agent_and_token(client, scope=["tools:read"])

    # Register read tool (allowed by policy)
    client.post("/tools", json={
        "name": "read_records",
        "server": "postgres-db",
        "description": "Executes read-only queries",
        "risk_level": "low",
        "required_scope": "tools:read"
    })

    # Call tool via gateway
    mcp_call = {
        "jsonrpc": "2.0",
        "id": "req-1",
        "method": "tools/call",
        "params": {
            "name": "read_records",
            "arguments": {"query": "SELECT 1;"}
        }
    }
    call_res = client.post(
        "/mcp/postgres-db",
        headers={"Authorization": f"Bearer {token}"},
        json=mcp_call
    )
    assert call_res.status_code == 200

    # Retrieve baseline
    base_res = client.get(f"/baselines/{agent_id}")
    assert base_res.status_code == 200
    base_data = base_res.json()
    assert base_data["agent_id"] == agent_id
    assert "read_records" in base_data["known_tools"]
    assert base_data["total_calls"] == 1
    assert base_data["total_denials"] == 0


def test_novel_tool_probe_alert(client):
    agent_id, token = setup_agent_and_token(client, scope=["tools:read"])

    client.post("/tools", json={
        "name": "read_records",
        "server": "db-server",
        "description": "Reads data",
        "risk_level": "low",
        "required_scope": "tools:read"
    })
    client.post("/tools", json={
        "name": "read_novel_data",
        "server": "db-server",
        "description": "Novel read tool",
        "risk_level": "low",
        "required_scope": "tools:read"
    })

    # Execute 2 normal calls to establish baseline
    for i in range(2):
        client.post(
            "/mcp/db-server",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "jsonrpc": "2.0",
                "id": f"call-{i}",
                "method": "tools/call",
                "params": {"name": "read_records", "arguments": {}}
            }
        )

    # Now invoke novel tool (allowed by policy, but new to agent's baseline)
    novel_res = client.post(
        "/mcp/db-server",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": "call-novel",
            "method": "tools/call",
            "params": {"name": "read_novel_data", "arguments": {}}
        }
    )
    assert novel_res.status_code == 200

    # Check alert generated
    alerts_res = client.get(f"/alerts?agent_id={agent_id}&rule=novel_tool_probe")
    assert alerts_res.status_code == 200
    alerts = alerts_res.json()
    assert len(alerts) >= 1
    assert alerts[0]["rule"] == "novel_tool_probe"
    assert alerts[0]["details"]["tool"] == "read_novel_data"


def test_denial_burst_automated_killswitch(client):
    # Agent only has read scope
    agent_id, token = setup_agent_and_token(client, scope=["tools:read"])

    # Register restricted tool requiring write
    client.post("/tools", json={
        "name": "drop_table",
        "server": "db-server",
        "description": "Drops table",
        "risk_level": "critical",
        "required_scope": "tools:write"
    })

    # Trigger 5 denials in succession (gateway maps policy deny to 403)
    for i in range(5):
        denied_call = client.post(
            "/mcp/db-server",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "jsonrpc": "2.0",
                "id": f"deny-{i}",
                "method": "tools/call",
                "params": {"name": "drop_table", "arguments": {}}
            }
        )
        assert denied_call.status_code == 403

    # Check alert generated with severity critical and action_taken suspend
    alerts_res = client.get(f"/alerts?agent_id={agent_id}&rule=denial_burst")
    assert alerts_res.status_code == 200
    alerts = alerts_res.json()
    assert len(alerts) == 1
    assert alerts[0]["severity"] == "critical"
    assert alerts[0]["action_taken"] == "suspend"
    assert alerts[0]["details"]["denied_count"] == 5

    # Check agent status
    agent_res = client.get(f"/agents/{agent_id}")
    assert agent_res.status_code == 200
    assert agent_res.json()["status"] == "suspended"

    # Subsequent gateway call should immediately fail with 403 Forbidden
    next_call = client.post(
        "/mcp/db-server",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": "blocked-call",
            "method": "tools/call",
            "params": {"name": "drop_table", "arguments": {}}
        }
    )
    assert next_call.status_code == 403
    detail_str = next_call.json()["detail"].lower()
    assert "kill switch" in detail_str or "terminated" in detail_str or "suspended" in detail_str


def test_alert_update_lifecycle(client):
    agent_id, token = setup_agent_and_token(client, scope=["tools:read"])

    client.post("/tools", json={
        "name": "forbidden_tool",
        "server": "s",
        "description": "forbidden",
        "risk_level": "high",
        "required_scope": "tools:admin"
    })

    # Trigger 5 denials to produce a denial_burst alert
    for i in range(5):
        client.post(
            "/mcp/s",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "jsonrpc": "2.0",
                "id": f"burst-{i}",
                "method": "tools/call",
                "params": {"name": "forbidden_tool", "arguments": {}}
            }
        )

    alerts = client.get(f"/alerts?agent_id={agent_id}").json()
    assert len(alerts) > 0
    alert_id = alerts[0]["id"]
    assert alerts[0]["status"] == "active"

    # Acknowledge alert
    patch_res = client.patch(f"/alerts/{alert_id}", json={"status": "acknowledged"})
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "acknowledged"

    # Resolve alert
    patch_res = client.patch(f"/alerts/{alert_id}", json={"status": "resolved"})
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "resolved"

    # Filter resolved
    resolved = client.get(f"/alerts?status=resolved").json()
    assert any(a["id"] == alert_id for a in resolved)
