from datetime import datetime, timedelta
import pytest
from anubis.services.auth.service import token_service
from anubis.services.approvals.models import ApprovalRequest


@pytest.fixture
def agent_and_token_for_approval(client):
    owner_resp = client.post("/owners", json={"name": "Ops Lead", "email": "ops_lead@corp.local"})
    owner_id = owner_resp.json()["id"]

    agent_resp = client.post("/agents", json={
        "name": "Finance-Exec-Agent",
        "owner_id": owner_id,
        "purpose": "Financial disbursements",
        "risk_tier": "high"
    })
    agent_id = agent_resp.json()["agent"]["id"]

    client.post("/tools", json={
        "name": "execute_transfer",
        "server": "finance",
        "required_scope": "tools:finance"
    })

    issued = token_service.issue_token(
        agent_id=agent_id,
        instance_id="inst-fin-1",
        scope=["tools:finance"],
        task_id="task-disburse-99",
        on_behalf_of="cfo@corp.local"
    )
    return {
        "agent_id": agent_id,
        "token": issued["access_token"]
    }


def test_approval_hold_and_resume_flow(client, agent_and_token_for_approval):
    token = agent_and_token_for_approval["token"]
    agent_id = agent_and_token_for_approval["agent_id"]

    # 1. Agent attempts high-value transfer ($25,000 > $5,000 policy threshold)
    resp_hold = client.post(
        "/mcp/finance",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "execute_transfer",
                "arguments": {"amount": 25000, "destination": "Strategic-Partner-LLC"}
            }
        }
    )
    assert resp_hold.status_code == 200
    res_data = resp_hold.json()["result"]
    assert res_data["status"] == "pending_approval"
    approval_id = res_data["approval_id"]
    assert approval_id.startswith("appr_")

    # 2. Check Approvals Queue
    list_resp = client.get("/approvals?status=pending")
    assert list_resp.status_code == 200
    pending_items = list_resp.json()
    assert any(a["id"] == approval_id for a in pending_items)

    # 3. Human Supervisor approves the request
    decision_resp = client.post(
        f"/approvals/{approval_id}/decision",
        json={
            "decision": "approved",
            "approver_id": "cfo@corp.local",
            "comment": "Verified invoice and partner contract. Approved."
        }
    )
    assert decision_resp.status_code == 200
    assert decision_resp.json()["status"] == "approved"
    assert decision_resp.json()["approver_id"] == "cfo@corp.local"

    # 4. Agent resumes execution by providing the approval_id
    resp_resume = client.post(
        "/mcp/finance",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "execute_transfer",
                "arguments": {
                    "amount": 25000,
                    "destination": "Strategic-Partner-LLC",
                    "approval_id": approval_id
                }
            }
        }
    )
    assert resp_resume.status_code == 200
    exec_result = resp_resume.json()["result"]
    assert exec_result["status"] == "transferred"
    assert exec_result["amount"] == 25000

    # 5. Single-Use Verification: Reusing the same approval_id MUST be rejected!
    resp_reuse = client.post(
        "/mcp/finance",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "execute_transfer",
                "arguments": {
                    "amount": 25000,
                    "destination": "Strategic-Partner-LLC",
                    "approval_id": approval_id
                }
            }
        }
    )
    assert resp_reuse.status_code == 200 or resp_reuse.status_code == 403
    err = resp_reuse.json().get("detail") or resp_reuse.json().get("error", {}).get("message", "")
    assert "consumed" in err.lower() or "invalid" in err.lower()


def test_rejection_of_approval_request(client, agent_and_token_for_approval):
    token = agent_and_token_for_approval["token"]

    # 1. Trigger pending approval
    resp_hold = client.post(
        "/mcp/finance",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {
                "name": "execute_transfer",
                "arguments": {"amount": 50000, "destination": "Untrusted-Entity"}
            }
        }
    )
    approval_id = resp_hold.json()["result"]["approval_id"]

    # 2. Supervisor rejects
    rej_resp = client.post(
        f"/approvals/{approval_id}/decision",
        json={
            "decision": "rejected",
            "approver_id": "compliance_officer@corp.local",
            "comment": "Suspicious destination. Blocked."
        }
    )
    assert rej_resp.status_code == 200
    assert rej_resp.json()["status"] == "rejected"

    # 3. Agent attempts to call with rejected approval
    resp_resume = client.post(
        "/mcp/finance",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 11,
            "method": "tools/call",
            "params": {
                "name": "execute_transfer",
                "arguments": {
                    "amount": 50000,
                    "destination": "Untrusted-Entity",
                    "approval_id": approval_id
                }
            }
        }
    )
    err = resp_resume.json().get("detail") or resp_resume.json().get("error", {}).get("message", "")
    assert "invalid" in err.lower() or "denied" in err.lower()
