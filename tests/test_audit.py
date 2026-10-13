import pytest
from anubis.services.auth.service import token_service
from anubis.services.auth.crypto import generate_es256_keypair, derive_cryptographic_agent_id
from anubis.services.audit.models import AuditEvent


def test_agent_cryptographic_unique_id_created_at_registration(client):
    """
    Validates that the unique cryptographic ID is created when the agent is registered,
    atomically derived from its public key fingerprint, not as an individual task.
    """
    owner_resp = client.post("/owners", json={"name": "Audit Admin", "email": "audit_admin@corp.local"})
    owner_id = owner_resp.json()["id"]

    # 1. Register with auto-generated keypair
    resp_auto = client.post("/agents", json={
        "name": "Auto-Crypto-Agent",
        "owner_id": owner_id,
        "purpose": "Verify atomic cryptographic ID generation"
    })
    assert resp_auto.status_code == 201
    agent_auto = resp_auto.json()["agent"]
    assert agent_auto["id"].startswith("agt_")
    # Verify ID matches derived fingerprint of returned public key
    expected_id = derive_cryptographic_agent_id(agent_auto["public_key"])
    assert agent_auto["id"] == expected_id

    # 2. Register with custom pre-generated keypair
    priv, pub = generate_es256_keypair()
    expected_custom_id = derive_cryptographic_agent_id(pub)
    resp_custom = client.post("/agents", json={
        "name": "Custom-Crypto-Agent",
        "owner_id": owner_id,
        "purpose": "Verify deterministic public key fingerprint ID",
        "public_key": pub
    })
    assert resp_custom.status_code == 201
    agent_custom = resp_custom.json()["agent"]
    assert agent_custom["id"] == expected_custom_id


def test_audit_hash_chain_logged_on_gateway_calls(client):
    owner_resp = client.post("/owners", json={"name": "Sec Lead", "email": "sec_lead@corp.local"})
    owner_id = owner_resp.json()["id"]

    agent_resp = client.post("/agents", json={
        "name": "Audit-Pipeline-Agent",
        "owner_id": owner_id,
        "purpose": "Test hash-chained audit logging"
    })
    agent_id = agent_resp.json()["agent"]["id"]

    # Register tool
    client.post("/tools", json={
        "name": "read_records",
        "server": "corp-db",
        "required_scope": "tools:read"
    })

    # Issue token
    issued = token_service.issue_token(
        agent_id=agent_id,
        instance_id="inst-audit-1",
        scope=["tools:read"],
        task_id="task-audit-001"
    )
    token = issued["access_token"]

    # 1. Successful tool call (allow)
    resp1 = client.post(
        "/mcp/corp-db",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "read_records", "arguments": {"limit": 10}}
        }
    )
    assert resp1.status_code == 200

    # 2. Denied tool call (missing scope)
    resp2 = client.post(
        "/mcp/corp-db",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "delete_database", "arguments": {}}
        }
    )
    assert resp2.status_code == 403

    # 3. Query audit trail
    audit_resp = client.get("/audit")
    assert audit_resp.status_code == 200
    events = audit_resp.json()
    assert len(events) >= 2

    # Check Hash Chaining properties
    first_event = events[0]
    second_event = events[1]

    assert first_event["seq"] == 1
    assert first_event["prev_hash"] == "0" * 64
    assert first_event["decision"] == "allow"
    assert first_event["outcome"] == "success"

    assert second_event["seq"] == 2
    assert second_event["prev_hash"] == first_event["hash"]  # Chained to previous event hash!
    assert second_event["decision"] == "deny"
    assert second_event["outcome"] == "denied"

    # 4. Cryptographic verification of intact chain
    verify_resp = client.get("/audit/verify")
    assert verify_resp.status_code == 200
    v_data = verify_resp.json()
    assert v_data["verified"] is True
    assert v_data["total_records"] >= 2
    assert v_data["latest_seq"] == 2


def test_audit_secret_redaction(client):
    owner_resp = client.post("/owners", json={"name": "Redaction Lead", "email": "redact@corp.local"})
    owner_id = owner_resp.json()["id"]

    agent_resp = client.post("/agents", json={
        "name": "Redaction-Agent",
        "owner_id": owner_id,
        "purpose": "Verify secret redaction in audit logs"
    })
    agent_id = agent_resp.json()["agent"]["id"]

    client.post("/tools", json={
        "name": "read_vault",
        "server": "vault",
        "required_scope": "tools:read"
    })

    issued = token_service.issue_token(agent_id=agent_id, instance_id="inst-1", scope=["tools:read"])
    token = issued["access_token"]

    # Tool call containing sensitive argument keys
    client.post(
        "/mcp/vault",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "read_vault",
                "arguments": {
                    "resource": "user_profiles",
                    "api_key": "raw_super_secret_api_key_12345",
                    "password": "MasterAdminPassword!",
                    "access_token": "sec_live_9948281928"
                }
            }
        }
    )

    events_resp = client.get("/audit?tool=read_vault")
    events = events_resp.json()
    assert len(events) >= 1
    logged_args = events[0]["args_redacted"]

    # Verify secrets are scrubbed
    assert logged_args["resource"] == "user_profiles"
    assert logged_args["api_key"] == "[REDACTED_SECRET]"
    assert logged_args["password"] == "[REDACTED_SECRET]"
    assert logged_args["access_token"] == "[REDACTED_SECRET]"


def test_tamper_detection_on_altered_record(client, db_session):
    owner_resp = client.post("/owners", json={"name": "Forensics", "email": "forensics@corp.local"})
    owner_id = owner_resp.json()["id"]

    agent_resp = client.post("/agents", json={"name": "Forensic-Agent", "owner_id": owner_id, "purpose": "Testing"})
    agent_id = agent_resp.json()["agent"]["id"]

    client.post("/tools", json={"name": "read_audit", "server": "sec", "required_scope": "tools:read"})
    issued = token_service.issue_token(agent_id=agent_id, instance_id="inst-1", scope=["tools:read"])
    token = issued["access_token"]

    # Produce 2 audit events
    client.post("/mcp/sec", headers={"Authorization": f"Bearer {token}"}, json={
        "jsonrpc": "2.0", "method": "tools/call", "params": {"name": "read_audit", "arguments": {}}
    })
    client.post("/mcp/sec", headers={"Authorization": f"Bearer {token}"}, json={
        "jsonrpc": "2.0", "method": "tools/call", "params": {"name": "read_audit", "arguments": {}}
    })

    # Prior to tampering, chain MUST verify
    clean_verify = client.get("/audit/verify")
    assert clean_verify.json()["verified"] is True

    # Maliciously tamper with record 1 in the database directly
    first_record = db_session.query(AuditEvent).filter(AuditEvent.seq == 1).first()
    first_record.decision = "deny"  # Altered content
    db_session.commit()

    # Cryptographic verification MUST flag the tampering
    tampered_verify = client.get("/audit/verify")
    t_data = tampered_verify.json()
    assert t_data["verified"] is False
    assert t_data["broken_at_seq"] == 1
    assert "tampering detected" in t_data["reason"].lower()
