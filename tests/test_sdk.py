import pytest
from anubis.sdk import AnubisClient, AnubisAgent
from anubis.sdk.exceptions import (
    AnubisPolicyDeniedError,
    AnubisApprovalRequiredError,
    AnubisKillSwitchError,
    AnubisAuthError
)


def test_sdk_registration_and_authentication(client):
    sdk_client = AnubisClient(http_client=client)

    # 1. Register owner
    owner = sdk_client.register_owner(name="Ops Admin", email="ops@corp.local", team="SecOps")
    assert "id" in owner

    # 2. Register agent
    agent_data = sdk_client.register_agent(
        name="SDK-Test-Agent",
        owner_id=owner["id"],
        purpose="Testing SDK client methods",
        risk_tier="low",
        capabilities=["tools:read"]
    )
    assert sdk_client.agent_id.startswith("agt_")
    assert sdk_client.private_key_pem is not None

    # 3. Authenticate
    token = sdk_client.authenticate(scope=["tools:read"])
    assert token is not None
    assert sdk_client.access_token == token


def test_sdk_tool_invocation_and_credential_isolation(client):
    sdk_client = AnubisClient(http_client=client)
    owner = sdk_client.register_owner(name="Ops Admin 2", email="ops2@corp.local")
    sdk_client.register_agent(
        name="SDK-Tool-Agent",
        owner_id=owner["id"],
        purpose="Tool invocation",
        capabilities=["tools:read"]
    )
    sdk_client.authenticate(scope=["tools:read"])

    # Register read tool with downstream secret
    client.post("/tools", json={
        "name": "read_records",
        "server": "corp-db",
        "description": "Reads records",
        "risk_level": "low",
        "required_scope": "tools:read",
        "downstream_credential_ref": "DB_SECRET",
        "downstream_secret_value": "super_secret_db_pass_12345"
    })

    # Invoke tool via SDK
    res = sdk_client.invoke_tool(
        server="corp-db",
        tool_name="read_records",
        arguments={"table": "logs"}
    )
    assert res["status"] in ("success", "executed")
    assert "super_secret_db_pass_12345" not in str(res)


def test_sdk_delegation_and_monotonic_narrowing(client):
    sdk_client = AnubisClient(http_client=client)
    owner = sdk_client.register_owner(name="Ops Admin 3", email="ops3@corp.local")

    primary_agent = AnubisAgent(
        name="Primary-Orchestrator",
        owner_id=owner["id"],
        purpose="Workflow orchestration",
        risk_tier="medium",
        capabilities=["tools:read", "tools:finance"],
        client=sdk_client
    )
    primary_agent.bootstrap(scope=["tools:read", "tools:finance"])

    # Register tools
    client.post("/tools", json={
        "name": "read_records",
        "server": "db",
        "description": "Reads data",
        "risk_level": "low",
        "required_scope": "tools:read"
    })
    client.post("/tools", json={
        "name": "execute_transfer",
        "server": "bank",
        "description": "Transfers funds",
        "risk_level": "medium",
        "required_scope": "tools:finance"
    })

    # Spawn sub-agent with narrowed scope (only tools:read)
    sub_agent = primary_agent.spawn_subagent(
        name="Worker-Sub",
        purpose="Data extraction",
        task_intent="Extraction of corporate records",
        delegated_scope=["tools:read"]
    )

    # Sub-agent executes allowed read tool
    sub_res = sub_agent.execute_tool(server="db", tool_name="read_records", arguments={})
    assert sub_res["status"] in ("success", "executed")

    # Sub-agent attempts privilege escalation on execute_transfer
    with pytest.raises(AnubisPolicyDeniedError) as exc_info:
        sub_agent.execute_tool(server="bank", tool_name="execute_transfer", arguments={"amount": 100})
    assert "tools:finance" in exc_info.value.reason.lower()


def test_sdk_human_approval_hold_and_resume(client):
    sdk_client = AnubisClient(http_client=client)
    owner = sdk_client.register_owner(name="Ops Admin 4", email="ops4@corp.local")

    agent = AnubisAgent(
        name="Finance-Agent",
        owner_id=owner["id"],
        purpose="Finance operations",
        risk_tier="medium",
        capabilities=["tools:finance"],
        client=sdk_client
    )
    agent.bootstrap(scope=["tools:finance"])

    client.post("/tools", json={
        "name": "execute_transfer",
        "server": "bank",
        "description": "Transfers funds",
        "risk_level": "critical",
        "required_scope": "tools:finance"
    })

    # $10,000 transfer requires approval
    with pytest.raises(AnubisApprovalRequiredError) as exc_info:
        agent.execute_tool(
            server="bank",
            tool_name="execute_transfer",
            arguments={"amount": 10000, "recipient": "vendor-corp"}
        )

    appr_err = exc_info.value
    assert appr_err.approval_id is not None
    assert appr_err.tool == "execute_transfer"

    # Approve via SDK
    dec_res = sdk_client.decide_approval(
        approval_id=appr_err.approval_id,
        decision="approved",
        approver_id="supervisor_bob@corp.local",
        comment="Approved by supervisor"
    )
    assert dec_res["status"] == "approved"

    # Resume tool execution with approval_id
    resumed = agent.execute_tool(
        server="bank",
        tool_name="execute_transfer",
        arguments={"amount": 10000, "recipient": "vendor-corp"},
        approval_id=appr_err.approval_id
    )
    assert resumed["status"] in ("success", "executed", "transferred")


def test_sdk_anomaly_detection_killswitch(client):
    sdk_client = AnubisClient(http_client=client)
    owner = sdk_client.register_owner(name="Ops Admin 5", email="ops5@corp.local")
    sdk_client.register_agent(
        name="Probing-Agent",
        owner_id=owner["id"],
        purpose="Denial probe testing",
        capabilities=["tools:read"]
    )
    sdk_client.authenticate(scope=["tools:read"])

    client.post("/tools", json={
        "name": "forbidden_cmd",
        "server": "s",
        "description": "Forbidden command",
        "risk_level": "high",
        "required_scope": "tools:admin"
    })

    # Trigger 5 denials through SDK
    for _ in range(5):
        with pytest.raises(AnubisPolicyDeniedError):
            sdk_client.invoke_tool(server="s", tool_name="forbidden_cmd", arguments={})

    # 6th invocation should raise AnubisKillSwitchError
    with pytest.raises(AnubisKillSwitchError):
        sdk_client.invoke_tool(server="s", tool_name="forbidden_cmd", arguments={})
