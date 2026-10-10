import time
import pytest
import jwt
from anubis.services.auth.crypto import (
    TokenService, sign_challenge, generate_es256_keypair
)
from anubis.services.auth.service import token_service


def test_valid_token_issuance_and_verification():
    ts = TokenService()
    issued = ts.issue_token(
        agent_id="agent-007",
        instance_id="inst-1",
        scope=["tools:exec", "tools:read"],
        task_id="task-recon",
        on_behalf_of="admin@corp.local",
        ttl_minutes=10
    )

    token_str = issued["access_token"]
    claims = ts.verify_token(token_str)

    assert claims["sub"] == "agent-007"
    assert claims["instance_id"] == "inst-1"
    assert claims["task_id"] == "task-recon"
    assert claims["on_behalf_of"] == "admin@corp.local"
    assert claims["scope"] == ["tools:exec", "tools:read"]
    assert claims["iss"] == "anubis-control-plane"
    assert claims["exp"] > time.time()


def test_expired_token_rejected():
    ts = TokenService()
    # Issue a token with 0 TTL / expired
    now = int(time.time()) - 300
    expired_payload = {
        "iss": "anubis-control-plane",
        "sub": "agent-expired",
        "instance_id": "inst-old",
        "act": ["agent-expired"],
        "on_behalf_of": "admin",
        "scope": ["tools:read"],
        "task_id": "task-old",
        "jti": "jti-expired-123",
        "iat": now - 300,
        "nbf": now - 300,
        "exp": now  # Expired 5 minutes ago
    }
    expired_token = jwt.encode(
        expired_payload,
        ts.private_key_pem,
        algorithm=ts.algorithm,
        headers={"kid": ts.kid}
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        ts.verify_token(expired_token)


def test_tampered_token_payload_rejected():
    ts = TokenService()
    issued = ts.issue_token(
        agent_id="agent-legit",
        instance_id="inst-legit",
        scope=["tools:read"],
        ttl_minutes=15
    )
    parts = issued["access_token"].split(".")
    header, payload_b64, sig = parts[0], parts[1], parts[2]

    # Maliciously attempt to escalate scope by replacing payload
    tampered_token = f"{header}.eyJzdWIiOiJhZ2VudC1sZWdpdCIsInNjb3BlIjpbInRvb2xzOmFkbWluIl19.{sig}"

    with pytest.raises(jwt.InvalidSignatureError):
        ts.verify_token(tampered_token)


def test_tampered_token_signature_rejected():
    ts = TokenService()
    issued = ts.issue_token(
        agent_id="agent-legit",
        instance_id="inst-legit",
        scope=["tools:read"],
        ttl_minutes=15
    )
    token = issued["access_token"]
    # Tamper with the last character of the signature
    corrupted_token = token[:-1] + ("A" if token[-1] != "A" else "B")

    with pytest.raises(jwt.InvalidSignatureError):
        ts.verify_token(corrupted_token)


def test_replayed_challenge_rejected(client):
    owner_resp = client.post("/owners", json={"name": "Replay Tester", "email": "replay@corp.local"})
    owner_id = owner_resp.json()["id"]

    agent_resp = client.post("/agents", json={
        "name": "Replay-Agent",
        "owner_id": owner_id,
        "purpose": "Verify replay protection"
    })
    agent_id = agent_resp.json()["agent"]["id"]
    priv_key_pem = agent_resp.json()["private_key_pem"]

    challenge_resp = client.post("/auth/challenge", json={"agent_id": agent_id})
    c_data = challenge_resp.json()
    sig = sign_challenge(priv_key_pem, c_data["challenge"])

    # First consumption succeeds
    token_resp_1 = client.post("/auth/token", json={
        "agent_id": agent_id,
        "instance_id": "inst-1",
        "challenge_id": c_data["challenge_id"],
        "signature": sig
    })
    assert token_resp_1.status_code == 200

    # Second consumption of identical challenge MUST fail (replay attack prevented)
    token_resp_2 = client.post("/auth/token", json={
        "agent_id": agent_id,
        "instance_id": "inst-1",
        "challenge_id": c_data["challenge_id"],
        "signature": sig
    })
    assert token_resp_2.status_code == 401
    assert "replay attack detected" in token_resp_2.json()["detail"].lower()


def test_suspended_and_revoked_agent_cannot_authenticate(client):
    owner_resp = client.post("/owners", json={"name": "Dana", "email": "dana@corp.local"})
    owner_id = owner_resp.json()["id"]

    agent_resp = client.post("/agents", json={
        "name": "Target-Agent",
        "owner_id": owner_id,
        "purpose": "Kill switch test"
    })
    agent_id = agent_resp.json()["agent"]["id"]

    # 1. Suspend agent
    client.patch(f"/agents/{agent_id}", json={"status": "suspended"})
    c_resp = client.post("/auth/challenge", json={"agent_id": agent_id})
    assert c_resp.status_code == 403
    assert "suspended" in c_resp.json()["detail"].lower()

    # 2. Revoke agent
    client.patch(f"/agents/{agent_id}", json={"status": "revoked"})
    c_resp_2 = client.post("/auth/challenge", json={"agent_id": agent_id})
    assert c_resp_2.status_code == 403
    assert "revoked" in c_resp_2.json()["detail"].lower()
