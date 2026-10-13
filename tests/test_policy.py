import asyncio
import pytest
from anubis.services.policy.schemas import (
    PolicyEvaluationInput, AgentContext, TokenContext, ActionContext
)
from anubis.services.policy.evaluator import policy_evaluator


def test_policy_allow_read_tool():
    eval_input = PolicyEvaluationInput(
        agent=AgentContext(id="agent-reader", risk_tier="low"),
        token=TokenContext(sub="agent-reader", scope=["tools:read"]),
        action=ActionContext(tool="read_data", server="database", arguments={})
    )
    decision = asyncio.run(policy_evaluator.evaluate(eval_input))
    assert decision.decision == "allow"
    assert "tools:read" in decision.reason


def test_policy_deny_missing_scope():
    eval_input = PolicyEvaluationInput(
        agent=AgentContext(id="agent-unscoped", risk_tier="low"),
        token=TokenContext(sub="agent-unscoped", scope=["tools:other"]),
        action=ActionContext(tool="read_data", server="database", arguments={})
    )
    decision = asyncio.run(policy_evaluator.evaluate(eval_input))
    assert decision.decision == "deny"
    assert "lacks" in decision.reason.lower()


def test_policy_internal_vs_external_email():
    # 1. Internal email allowed
    internal_input = PolicyEvaluationInput(
        agent=AgentContext(id="agent-mailer", risk_tier="medium"),
        token=TokenContext(sub="agent-mailer", scope=["tools:email"]),
        action=ActionContext(
            tool="send_email",
            server="mail",
            arguments={"recipient": "security@corp.local", "subject": "Alert"}
        )
    )
    res_internal = asyncio.run(policy_evaluator.evaluate(internal_input))
    assert res_internal.decision == "allow"

    # 2. External email requires human approval
    external_input = PolicyEvaluationInput(
        agent=AgentContext(id="agent-mailer", risk_tier="medium"),
        token=TokenContext(sub="agent-mailer", scope=["tools:email"]),
        action=ActionContext(
            tool="send_email",
            server="mail",
            arguments={"recipient": "exfiltrate@external-evil.com", "subject": "Data"}
        )
    )
    res_external = asyncio.run(policy_evaluator.evaluate(external_input))
    assert res_external.decision == "require_approval"
    assert "external email" in res_external.reason.lower()


def test_policy_financial_transaction_threshold():
    # Normal transaction below $5000 -> allowed
    normal_tx = PolicyEvaluationInput(
        agent=AgentContext(id="agent-fin", risk_tier="high"),
        token=TokenContext(sub="agent-fin", scope=["tools:finance"]),
        action=ActionContext(
            tool="execute_transfer",
            server="finance",
            arguments={"amount": 1200.0, "destination": "Vendor-A"}
        )
    )
    res_normal = asyncio.run(policy_evaluator.evaluate(normal_tx))
    assert res_normal.decision == "allow"

    # High-value transaction above $5000 -> requires human approval
    large_tx = PolicyEvaluationInput(
        agent=AgentContext(id="agent-fin", risk_tier="high"),
        token=TokenContext(sub="agent-fin", scope=["tools:finance"]),
        action=ActionContext(
            tool="execute_transfer",
            server="finance",
            arguments={"amount": 25000.0, "destination": "Offshore-LLC"}
        )
    )
    res_large = asyncio.run(policy_evaluator.evaluate(large_tx))
    assert res_large.decision == "require_approval"
    assert "exceeds $5,000" in res_large.reason


def test_policy_dangerous_tool_denied_for_low_tier():
    shell_input = PolicyEvaluationInput(
        agent=AgentContext(id="agent-low", risk_tier="low"),
        token=TokenContext(sub="agent-low", scope=["tools:admin", "tools:read"]),
        action=ActionContext(tool="system_shell", server="system", arguments={"command": "whoami"})
    )
    decision = asyncio.run(policy_evaluator.evaluate(shell_input))
    assert decision.decision == "deny"
    assert "prohibited" in decision.reason.lower()


def test_policy_registration_and_simulation_api(client):
    # Register policy
    resp = client.post("/policies", json={
        "name": "corporate-security-baseline",
        "version": "1.0.0",
        "description": "Baseline corporate IAM security policy",
        "rego_source": "package anubis.authz\ndefault decision = 'deny'"
    })
    assert resp.status_code == 201
    assert resp.json()["name"] == "corporate-security-baseline"

    # List policies
    list_resp = client.get("/policies")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1

    # Simulate via API
    sim_resp = client.post("/policies/simulate", json={
        "agent": {"id": "agent-1", "risk_tier": "low"},
        "token": {"sub": "agent-1", "scope": ["tools:read"]},
        "action": {"tool": "read_data", "server": "records", "arguments": {}}
    })
    assert sim_resp.status_code == 200
    assert sim_resp.json()["decision"] == "allow"
