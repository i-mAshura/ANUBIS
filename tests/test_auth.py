import pytest
from anubis.services.auth.crypto import sign_challenge, generate_es256_keypair


def test_jwks_endpoint(client):
    resp = client.get("/.well-known/jwks.json")
    assert resp.status_code == 200
    jwks = resp.json()
    assert "keys" in jwks
    assert len(jwks["keys"]) >= 1
    key = jwks["keys"][0]
    assert key["kty"] == "EC"
    assert key["crv"] == "P-256"
    assert "x" in key
    assert "y" in key
    assert key["use"] == "sig"


def test_full_challenge_response_authentication(client):
    # 1. Register owner & agent
    owner_resp = client.post("/owners", json={"name": "Alice", "email": "alice_auth@corp.local"})
    owner_id = owner_resp.json()["id"]

    agent_resp = client.post("/agents", json={
        "name": "Auth-Test-Agent",
        "owner_id": owner_id,
        "purpose": "Verify challenge-response flow"
    })
    agent_data = agent_resp.json()["agent"]
    agent_id = agent_data["id"]
    priv_key_pem = agent_resp.json()["private_key_pem"]

    # 2. Request Challenge
    challenge_resp = client.post("/auth/challenge", json={
        "agent_id": agent_id,
        "instance_id": "inst-worker-1"
    })
    assert challenge_resp.status_code == 201
    c_data = challenge_resp.json()
    challenge_id = c_data["challenge_id"]
    challenge_str = c_data["challenge"]

    # 3. Sign Challenge with agent's private key
    sig = sign_challenge(priv_key_pem, challenge_str)

    # 4. Exchange for Token
    token_resp = client.post("/auth/token", json={
        "agent_id": agent_id,
        "instance_id": "inst-worker-1",
        "challenge_id": challenge_id,
        "signature": sig,
        "task_id": "task-audit-101",
        "on_behalf_of": "alice",
        "requested_scope": ["tools:database:read", "tools:search"]
    })
    assert token_resp.status_code == 200
    t_data = token_resp.json()
    assert "access_token" in t_data
    assert t_data["token_type"] == "Bearer"
    assert t_data["claims"]["sub"] == agent_id
    assert t_data["claims"]["instance_id"] == "inst-worker-1"
    assert t_data["claims"]["task_id"] == "task-audit-101"
    assert t_data["claims"]["on_behalf_of"] == "alice"
    assert "tools:database:read" in t_data["claims"]["scope"]


def test_auth_wrong_signature_fails(client):
    owner_resp = client.post("/owners", json={"name": "Bob", "email": "bob_auth@corp.local"})
    owner_id = owner_resp.json()["id"]

    agent_resp = client.post("/agents", json={
        "name": "Wrong-Key-Agent",
        "owner_id": owner_id,
        "purpose": "Test signature mismatch"
    })
    agent_id = agent_resp.json()["agent"]["id"]

    challenge_resp = client.post("/auth/challenge", json={"agent_id": agent_id})
    c_data = challenge_resp.json()

    # Sign with a completely different keypair
    unrelated_priv, _ = generate_es256_keypair()
    invalid_sig = sign_challenge(unrelated_priv, c_data["challenge"])

    token_resp = client.post("/auth/token", json={
        "agent_id": agent_id,
        "instance_id": "inst-1",
        "challenge_id": c_data["challenge_id"],
        "signature": invalid_sig
    })
    assert token_resp.status_code == 401
    assert "verification failed" in token_resp.json()["detail"].lower()
