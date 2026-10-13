import os
import httpx
from datetime import datetime
from typing import Dict, Any, Optional
from anubis.services.policy.schemas import PolicyEvaluationInput, PolicyDecisionResponse


class PolicyEvaluator:
    def __init__(self, opa_url: Optional[str] = None):
        self.opa_url = opa_url or os.getenv("OPA_URL", "http://localhost:8181")

    async def evaluate_remote_opa(self, eval_input: PolicyEvaluationInput) -> Optional[PolicyDecisionResponse]:
        """
        Attempts to evaluate policy against an external Open Policy Agent (OPA) server.
        Endpoint: POST {opa_url}/v1/data/anubis/authz
        """
        try:
            async with httpx.AsyncClient(timeout=1.5) as client:
                resp = await client.post(
                    f"{self.opa_url}/v1/data/anubis/authz",
                    json={"input": eval_input.model_dump()}
                )
                if resp.status_code == 200:
                    data = resp.json().get("result", {})
                    decision = data.get("decision")
                    reason = data.get("reason", "OPA policy decision")
                    if decision in ["allow", "deny", "require_approval"]:
                        return PolicyDecisionResponse(
                            decision=decision,
                            reason=reason,
                            rule_matched="opa_remote_rego",
                            evaluated_at=datetime.utcnow()
                        )
        except Exception:
            # Fall back to local embedded evaluator or fail closed if configured
            pass
        return None

    def evaluate_local(self, eval_input: PolicyEvaluationInput) -> PolicyDecisionResponse:
        """
        Local deterministic policy engine mirroring the Rego policy specifications.
        Guarantees zero-dependency, fail-closed enforcement.
        """
        try:
            tool = eval_input.action.tool
            server = eval_input.action.server
            arguments = eval_input.action.arguments
            scopes = set(eval_input.token.scope)
            risk_tier = eval_input.agent.risk_tier

            # Rule 1: Dangerous tools are strictly denied for non-critical agents
            if tool in ["system_shell", "execute_command", "drop_table", "delete_database"]:
                if risk_tier != "critical" or "tools:admin" not in scopes:
                    return PolicyDecisionResponse(
                        decision="deny",
                        reason="System shell / dangerous tool execution prohibited for agent tier.",
                        rule_matched="deny_dangerous_tools"
                    )

            # Rule 2: Email tools require tools:email scope & domain constraints
            if tool in ["send_email", "dispatch_mail"]:
                if "tools:email" not in scopes and "tools:write" not in scopes:
                    return PolicyDecisionResponse(
                        decision="deny",
                        reason=f"Token lacks required scope 'tools:email' to invoke '{tool}'.",
                        rule_matched="scope_enforcement"
                    )

                recipient = str(arguments.get("recipient", "")).lower()
                # External email recipients require human approval
                if recipient and not recipient.endswith("@corp.local"):
                    return PolicyDecisionResponse(
                        decision="require_approval",
                        reason=f"External email recipient '{recipient}' requires human supervisor approval.",
                        rule_matched="external_email_approval"
                    )
                return PolicyDecisionResponse(
                    decision="allow",
                    reason="Internal email permitted by tools:email scope.",
                    rule_matched="allow_internal_email"
                )

            # Rule 3: Financial tools require tools:finance scope & transaction thresholds
            if tool in ["execute_transfer", "transfer_funds", "write_ledger"]:
                if "tools:finance" not in scopes:
                    return PolicyDecisionResponse(
                        decision="deny",
                        reason=f"Token lacks 'tools:finance' scope required for '{tool}'.",
                        rule_matched="scope_enforcement"
                    )

                amount = float(arguments.get("amount", 0))
                if amount > 5000:
                    return PolicyDecisionResponse(
                        decision="require_approval",
                        reason=f"Financial transaction of ${amount:,.2f} exceeds $5,000 threshold and requires human approval.",
                        rule_matched="financial_threshold_approval"
                    )
                return PolicyDecisionResponse(
                    decision="allow",
                    reason="Financial transaction within authorized limit.",
                    rule_matched="allow_financial_transaction"
                )

            # Rule 4: Read tools require tools:read or tools:all
            if tool.startswith("read_") or tool.startswith("get_") or tool in ["search_docs", "fetch_records"]:
                if "tools:read" in scopes or "tools:all" in scopes:
                    return PolicyDecisionResponse(
                        decision="allow",
                        reason=f"Read access permitted by tools:read scope for '{tool}'.",
                        rule_matched="allow_read_tools"
                    )
                return PolicyDecisionResponse(
                    decision="deny",
                    reason=f"Token lacks 'tools:read' scope to execute '{tool}'.",
                    rule_matched="scope_enforcement"
                )

            # Rule 5: Generic tools check matching scope
            required_scope = f"tools:{server}"
            if required_scope in scopes or "tools:all" in scopes:
                return PolicyDecisionResponse(
                    decision="allow",
                    reason=f"Scope '{required_scope}' grants access to tool '{tool}'.",
                    rule_matched="allow_scoped_tool"
                )

            # Default fail-closed: DENY
            return PolicyDecisionResponse(
                decision="deny",
                reason=f"Default deny: no matching allow rule or required scope for tool '{tool}'.",
                rule_matched="default_deny"
            )

        except Exception as exc:
            # Absolute Fail-Closed invariant
            return PolicyDecisionResponse(
                decision="deny",
                reason=f"Policy evaluation failure: {str(exc)} (Fail-Closed)",
                rule_matched="fail_closed_exception"
            )

    async def evaluate(self, eval_input: PolicyEvaluationInput) -> PolicyDecisionResponse:
        # Try remote OPA first if configured and reachable
        remote_decision = await self.evaluate_remote_opa(eval_input)
        if remote_decision:
            return remote_decision
        
        # Fallback to local evaluation
        return self.evaluate_local(eval_input)


policy_evaluator = PolicyEvaluator()
