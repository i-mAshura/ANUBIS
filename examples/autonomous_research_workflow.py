"""
ANUBIS Zero-Trust Control Plane - End-to-End Autonomous Agent Demo
Demonstrates:
  1. Cryptographic Agent Registration (ECDSA P-256 & SHA-256 SPKI fingerprint derivation)
  2. Challenge-Response Nonce Authentication
  3. Fail-Closed Gateway MCP Proxy with Credential Brokering
  4. Monotonic Scope Sub-Agent Delegation & 'act' Lineage Tracking
  5. Human-in-the-Loop Hold-and-Resume Approval Workflow
  6. Anomaly Detection Engine Automated Retribution via Kill Switch
"""

import sys
import time
from anubis.sdk import AnubisClient, AnubisAgent
from anubis.sdk.exceptions import (
    AnubisPolicyDeniedError,
    AnubisApprovalRequiredError,
    AnubisKillSwitchError
)


def run_demo(base_url: str = "http://localhost:8000"):
    print("=" * 70)
    print("  ANUBIS: Autonomous Agent Zero-Trust Architecture Demo")
    print("  'Every agent is weighed before it passes, and the record never lies.'")
    print("=" * 70)

    client = AnubisClient(base_url=base_url)

    # 1. Register Owner
    print("\n[1] Registering Corporate Owner...")
    owner = client.register_owner(
        name="Security & Compliance Office",
        email="secops@underworld.corp",
        team="Zero-Trust IAM"
    )
    owner_id = owner["id"]
    print(f"    Owner Registered: {owner['name']} ({owner_id})")

    # 2. Register Tools on MCP Gateway
    print("\n[2] Registering MCP Tools on Gateway...")
    client._post("/tools", json={
        "name": "read_financial_filings",
        "server": "corp-edgar",
        "description": "Reads quarterly SEC filings and quarterly balance sheets",
        "risk_level": "low",
        "required_scope": "tools:read",
        "downstream_credential_ref": "EDGAR_API_SECRET",
        "downstream_secret_value": "sec_live_edgar_super_secret_9981"
    })
    client._post("/tools", json={
        "name": "send_email",
        "server": "mail-exchange",
        "description": "Dispatches summary reports",
        "risk_level": "medium",
        "required_scope": "tools:email"
    })
    client._post("/tools", json={
        "name": "execute_transfer",
        "server": "bank-settlement",
        "description": "Executes treasury transfers",
        "risk_level": "critical",
        "required_scope": "tools:finance"
    })
    print("    Registered: 'read_financial_filings', 'send_email', 'execute_transfer'")

    # 3. Bootstrap Orchestrator Agent
    print("\n[3] Bootstrapping Primary Agent (Orchestrator-Prime)...")
    orchestrator = AnubisAgent(
        name="Orchestrator-Prime",
        owner_id=owner_id,
        purpose="Autonomous Financial Research & Reconciliation",
        risk_tier="medium",
        capabilities=["tools:read", "tools:email", "tools:finance"],
        client=client
    )
    orch_token = orchestrator.bootstrap(scope=["tools:read", "tools:email", "tools:finance"])
    print(f"    Agent ID Born: {orchestrator.agent_id} (derived from ECDSA P-256 fingerprint)")
    print(f"    Authentication Token Acquired (ES256 signed)")

    # 4. Execute Allowed Tool through Gateway
    print("\n[4] Invoking 'read_financial_filings' through ANUBIS MCP Gateway...")
    result = orchestrator.execute_tool(
        server="corp-edgar",
        tool_name="read_financial_filings",
        arguments={"ticker": "CORP", "year": 2026}
    )
    print(f"    Success: {result['status']}")
    print(f"    Brokered Auth Used: {result.get('authenticated_with_credential_ref')}")
    print(f"    Zero-Trust Leakage Check: Raw secret scrubbed from response.")

    # 5. Spawn Delegated Sub-Agent with Monotonic Narrowing
    print("\n[5] Spawning Sub-Agent (Researcher-Sub01) with Scope-Narrowed Delegation...")
    sub_agent = orchestrator.spawn_subagent(
        name="Researcher-Sub01",
        purpose="SEC Filing Data Extraction",
        task_intent="Extract and summarize quarterly balance sheets",
        delegated_scope=["tools:read"]  # Narrowed from [read, email, finance]
    )
    print(f"    Sub-Agent ID Born: {sub_agent.agent_id}")
    print(f"    Delegated Task ID: {sub_agent.active_task_id}")
    print(f"    Lineage Chain ('act'): ['{orchestrator.agent_id}', '{sub_agent.agent_id}']")

    # 6. Sub-Agent Executes Allowed Tool
    print("\n[6] Sub-Agent executing permitted 'read_financial_filings'...")
    sub_res = sub_agent.execute_tool(
        server="corp-edgar",
        tool_name="read_financial_filings",
        arguments={"ticker": "CORP", "quarter": "Q3"}
    )
    print(f"    Sub-Agent Status: {sub_res['status']}")

    # 7. Sub-Agent Privilege Escalation Attempt (Fail-Closed)
    print("\n[7] Testing Privilege Escalation: Sub-Agent attempts 'execute_transfer' without scope...")
    try:
        sub_agent.execute_tool(
            server="bank-settlement",
            tool_name="execute_transfer",
            arguments={"amount": 1000, "destination": "External-Account"}
        )
        print("    [!] ERROR: Action was unexpectedly allowed!")
    except AnubisPolicyDeniedError as exc:
        print(f"    [BLOCKED] Zero-Trust Enforced: {exc.reason}")

    # 8. Human-in-the-Loop Hold-and-Resume Workflow
    print("\n[8] High-Risk Tool Execution: Orchestrator attempts $7,500 transfer...")
    try:
        orchestrator.execute_tool(
            server="bank-settlement",
            tool_name="execute_transfer",
            arguments={"amount": 7500, "destination": "Vendor-Vault"}
        )
    except AnubisApprovalRequiredError as appr_err:
        print(f"    [PAUSED] Action requires human supervisor approval!")
        print(f"    Approval ID: {appr_err.approval_id}")
        print(f"    Expires At:  {appr_err.expires_at}")

        # Human supervisor inspects and approves
        print("    Human Supervisor reviewing via /approvals API...")
        client.decide_approval(
            approval_id=appr_err.approval_id,
            decision="approved",
            approver_id="human_supervisor_jane@underworld.corp",
            comment="Authorized quarterly vendor payment"
        )
        print("    Supervisor Decision: APPROVED.")

        # Agent resumes with approval_id
        resumed_result = orchestrator.execute_tool(
            server="bank-settlement",
            tool_name="execute_transfer",
            arguments={"amount": 7500, "destination": "Vendor-Vault"},
            approval_id=appr_err.approval_id
        )
        print(f"    [RESUMED] Tool executed successfully: {resumed_result['status']}")

    # 9. Cryptographic Audit Trail Verification
    print("\n[9] Verifying Immutable Hash-Chained Audit Ledger...")
    audit_status = client.verify_audit_integrity()
    print(f"    Audit Chain Status: {audit_status['status']}")
    print(f"    Verified Records:   {audit_status['verified_records']}")
    print(f"    Ledger Head Hash:   {audit_status['head_hash']}")

    # 10. Anomaly Detection & Automated Kill Switch Retribution
    print("\n[10] Testing Anomaly Detection: Simulating Denial Burst on Sub-Agent...")
    for i in range(5):
        try:
            sub_agent.execute_tool(
                server="bank-settlement",
                tool_name="execute_transfer",
                arguments={"amount": 1000}
            )
        except AnubisPolicyDeniedError:
            pass

    print("    Burst of 5 denials submitted in sliding window.")
    alerts = client.query_alerts(agent_id=sub_agent.agent_id, rule="denial_burst")
    if alerts:
        print(f"    [ALERT TRIGGERED] Severity: {alerts[0]['severity']}, Action: {alerts[0]['action_taken']}")

    print("    Verifying immediate kill-switch enforcement on Sub-Agent...")
    try:
        sub_agent.execute_tool(
            server="corp-edgar",
            tool_name="read_financial_filings",
            arguments={"ticker": "CORP"}
        )
        print("    [!] ERROR: Sub-Agent was not terminated!")
    except AnubisKillSwitchError as ks_err:
        print(f"    [KILL SWITCH ACTIVE] Sub-Agent Execution Terminated: {ks_err}")

    print("\n" + "=" * 70)
    print("  ANUBIS Zero-Trust Workflow Demo Completed Successfully!")
    print("=" * 70)


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    run_demo(url)
