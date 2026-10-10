import pytest
from anubis.services.auth.crypto import generate_es256_keypair


def test_create_and_get_owner(client):
    # Create owner
    resp = client.post("/owners", json={
        "name": "SecOps Team",
        "email": "secops@corp.local",
        "team": "Security Architecture"
    })
    assert resp.status_code == 201
    owner_data = resp.json()
    assert owner_data["name"] == "SecOps Team"
    assert "id" in owner_data

    # Duplicate email should fail
    resp_dup = client.post("/owners", json={
        "name": "SecOps Alt",
        "email": "secops@corp.local"
    })
    assert resp_dup.status_code == 409

    # Retrieve owner
    resp_get = client.get(f"/owners/{owner_data['id']}")
    assert resp_get.status_code == 200
    assert resp_get.json()["email"] == "secops@corp.local"


def test_register_agent_with_auto_keypair(client):
    # Create owner first
    owner_resp = client.post("/owners", json={"name": "Alice", "email": "alice@corp.local"})
    owner_id = owner_resp.json()["id"]

    # Register agent without public key (should auto-generate keypair)
    agent_resp = client.post("/agents", json={
        "name": "Sentinel-1",
        "owner_id": owner_id,
        "purpose": "Automated log auditing and triage",
        "framework": "langchain",
        "risk_tier": "medium"
    })
    assert agent_resp.status_code == 201
    data = agent_resp.json()
    assert data["agent"]["name"] == "Sentinel-1"
    assert data["agent"]["status"] == "active"
    assert "BEGIN PUBLIC KEY" in data["agent"]["public_key"]
    assert data["private_key_pem"] is not None
    assert "BEGIN PRIVATE KEY" in data["private_key_pem"]


def test_register_agent_with_custom_keypair(client):
    owner_resp = client.post("/owners", json={"name": "Bob", "email": "bob@corp.local"})
    owner_id = owner_resp.json()["id"]

    priv, pub = generate_es256_keypair()
    agent_resp = client.post("/agents", json={
        "name": "Researcher-Alpha",
        "owner_id": owner_id,
        "purpose": "Web data aggregation",
        "public_key": pub,
        "risk_tier": "low"
    })
    assert agent_resp.status_code == 201
    data = agent_resp.json()
    assert data["agent"]["public_key"] == pub
    # Since client provided public key, server should NOT return private key
    assert data["private_key_pem"] is None


def test_update_agent_status_suspend_and_revoke(client):
    owner_resp = client.post("/owners", json={"name": "Charlie", "email": "charlie@corp.local"})
    owner_id = owner_resp.json()["id"]

    agent_resp = client.post("/agents", json={
        "name": "Finance-Bot",
        "owner_id": owner_id,
        "purpose": "Invoice matching",
        "risk_tier": "high"
    })
    agent_id = agent_resp.json()["agent"]["id"]

    # Suspend agent
    patch_resp = client.patch(f"/agents/{agent_id}", json={"status": "suspended"})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["status"] == "suspended"

    # Revoke agent
    patch_resp = client.patch(f"/agents/{agent_id}", json={"status": "revoked"})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["status"] == "revoked"

    # Filter list
    list_revoked = client.get("/agents?status=revoked")
    assert list_revoked.status_code == 200
    assert len(list_revoked.json()) >= 1
    assert list_revoked.json()[0]["id"] == agent_id
