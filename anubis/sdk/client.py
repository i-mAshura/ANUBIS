import uuid
import httpx
from typing import Optional, Dict, Any, List

from anubis.services.auth.crypto import generate_es256_keypair, sign_challenge
from anubis.sdk.exceptions import (
    AnubisAuthError,
    AnubisPolicyDeniedError,
    AnubisApprovalRequiredError,
    AnubisKillSwitchError,
    AnubisError
)


class AnubisClient:
    """
    Python client for interacting with the ANUBIS Zero-Trust Control Plane.
    Manages local cryptographic identity, challenge-response token authentication,
    delegation exchange, and mediated MCP tool calls.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        agent_id: Optional[str] = None,
        private_key_pem: Optional[str] = None,
        public_key_pem: Optional[str] = None,
        http_client: Optional[Any] = None
    ):
        self.base_url = base_url.rstrip("/")
        self.agent_id = agent_id
        self.private_key_pem = private_key_pem
        self.public_key_pem = public_key_pem
        self._http = http_client or httpx.Client(base_url=self.base_url)
        self.access_token: Optional[str] = None

    def _post(self, path: str, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        return self._http.post(path, json=json, headers=headers)

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        return self._http.get(path, params=params, headers=headers)

    def _patch(self, path: str, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        return self._http.patch(path, json=json, headers=headers)

    # 1. Identity & Registration
    def register_owner(self, name: str, email: str, team: Optional[str] = None) -> Dict[str, Any]:
        resp = self._post("/owners", json={"name": name, "email": email, "team": team})
        if resp.status_code not in (200, 201):
            raise AnubisError(f"Owner registration failed: {resp.text}")
        return resp.json()

    def register_agent(
        self,
        name: str,
        owner_id: str,
        purpose: str,
        risk_tier: str = "low",
        capabilities: Optional[List[str]] = None,
        generate_local_key: bool = True
    ) -> Dict[str, Any]:
        """
        Registers an agent with ANUBIS.
        Generates local ECDSA P-256 keys so the private key never leaves the client boundary,
        and derives the atomic unique agent ID (agt_<fingerprint>).
        """
        if generate_local_key and not self.private_key_pem:
            self.private_key_pem, self.public_key_pem = generate_es256_keypair()

        payload = {
            "name": name,
            "owner_id": owner_id,
            "purpose": purpose,
            "risk_tier": risk_tier,
            "capabilities": capabilities or [],
            "public_key": self.public_key_pem
        }

        resp = self._post("/agents", json=payload)
        if resp.status_code not in (200, 201):
            raise AnubisError(f"Agent registration failed: {resp.text}")

        data = resp.json()
        self.agent_id = data["agent"]["id"]
        # If server generated a keypair because none was provided
        if "private_key_pem" in data and data["private_key_pem"]:
            self.private_key_pem = data["private_key_pem"]
            self.public_key_pem = data["agent"]["public_key"]

        return data

    # 2. Challenge-Response Authentication
    def authenticate(
        self,
        scope: Optional[List[str]] = None,
        instance_id: Optional[str] = None,
        task_id: Optional[str] = None
    ) -> str:
        """
        Performs cryptographic challenge-response authentication.
        1. Requests cryptographic nonce challenge from /auth/challenge
        2. Signs challenge with local ECDSA P-256 private key
        3. Trades signature for ES256 signed JWT
        """
        if not self.agent_id or not self.private_key_pem:
            raise AnubisAuthError("Agent ID and private key are required to authenticate.")

        chal_resp = self._post("/auth/challenge", json={"agent_id": self.agent_id})
        if chal_resp.status_code not in (200, 201):
            raise AnubisAuthError(f"Challenge request failed: {chal_resp.text}")

        chal_data = chal_resp.json()
        challenge_id = chal_data["challenge_id"]
        challenge_str = chal_data["challenge"]
        signature = sign_challenge(self.private_key_pem, challenge_str)

        instance = instance_id or f"inst-{uuid.uuid4().hex[:8]}"
        tok_resp = self._post("/auth/token", json={
            "agent_id": self.agent_id,
            "instance_id": instance,
            "challenge_id": challenge_id,
            "signature": signature,
            "requested_scope": scope or ["tools:read"],
            "task_id": task_id or "task-default"
        })

        if tok_resp.status_code != 200:
            raise AnubisAuthError(f"Authentication failed: {tok_resp.text}")

        tok_data = tok_resp.json()
        self.access_token = tok_data["access_token"]
        return self.access_token

    # 3. Gateway MCP Tool Execution
    def invoke_tool(
        self,
        server: str,
        tool_name: str,
        arguments: Optional[Dict[str, Any]] = None,
        approval_id: Optional[str] = None,
        custom_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes a tool through the ANUBIS Gateway MCP JSON-RPC 2.0 proxy.
        Enforces policy evaluation, credential brokering, and secret redaction.
        """
        token = custom_token or self.access_token
        if not token:
            raise AnubisAuthError("No active access token. Call authenticate() first.")

        args = dict(arguments or {})
        if approval_id:
            args["approval_id"] = approval_id

        payload = {
            "jsonrpc": "2.0",
            "id": f"call-{uuid.uuid4().hex[:8]}",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": args
            }
        }

        resp = self._post(
            f"/mcp/{server}",
            headers={"Authorization": f"Bearer {token}"},
            json=payload
        )

        if resp.status_code == 403:
            detail = resp.json().get("detail", "")
            detail_lower = detail.lower()
            if "kill switch" in detail_lower or "terminated" in detail_lower or "suspended" in detail_lower:
                raise AnubisKillSwitchError(f"Terminated by ANUBIS Kill Switch: {detail}")
            raise AnubisPolicyDeniedError(
                message=f"Access Denied by ANUBIS Policy: {detail}",
                tool=tool_name,
                reason=detail
            )

        if resp.status_code == 401:
            raise AnubisAuthError(f"Unauthorized: {resp.text}")

        if resp.status_code != 200:
            raise AnubisError(f"Gateway invocation failed ({resp.status_code}): {resp.text}")

        data = resp.json()

        # Handle pending human approval response
        if "result" in data and isinstance(data["result"], dict) and data["result"].get("status") == "pending_approval":
            res = data["result"]
            raise AnubisApprovalRequiredError(
                message=res.get("message", "Tool invocation paused for human supervisor approval"),
                approval_id=res["approval_id"],
                tool=tool_name,
                expires_at=res["expires_at"]
            )

        return data.get("result", {})

    # 4. Tasks & Sub-Agent Delegation
    def create_task(
        self,
        intent: str,
        on_behalf_of: str = "system",
        root_agent_id: Optional[str] = None,
        requested_scope: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        agent_id = root_agent_id or self.agent_id
        if not agent_id:
            raise AnubisError("Root agent ID is required to create a task.")
        resp = self._post("/tasks", json={
            "root_agent_id": agent_id,
            "on_behalf_of": on_behalf_of,
            "intent": intent,
            "requested_scope": requested_scope or ["tools:read"]
        })
        if resp.status_code not in (200, 201):
            raise AnubisError(f"Task creation failed: {resp.text}")
        return resp.json()

    def delegate_token(
        self,
        target_agent_id: str,
        task_id: str,
        requested_scope: List[str]
    ) -> Dict[str, Any]:
        """
        Exchanges current token for a delegated sub-agent token.
        Enforces monotonic scope narrowing and appends to the 'act' lineage chain.
        """
        if not self.access_token:
            raise AnubisAuthError("No active token to delegate from.")

        resp = self._post(
            "/auth/exchange",
            headers={"Authorization": f"Bearer {self.access_token}"},
            json={
                "child_agent_id": target_agent_id,
                "task_id": task_id,
                "requested_scope": requested_scope
            }
        )
        if resp.status_code != 200:
            raise AnubisError(f"Token delegation failed ({resp.status_code}): {resp.text}")
        return resp.json()

    # 5. Approvals Workflow
    def get_approval(self, approval_id: str) -> Dict[str, Any]:
        resp = self._get(f"/approvals/{approval_id}")
        if resp.status_code != 200:
            raise AnubisError(f"Failed to fetch approval {approval_id}: {resp.text}")
        return resp.json()

    def decide_approval(
        self,
        approval_id: str,
        decision: str,
        approver_id: str,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        resp = self._post(f"/approvals/{approval_id}/decision", json={
            "decision": decision,
            "approver_id": approver_id,
            "comment": comment or ""
        })
        if resp.status_code != 200:
            raise AnubisError(f"Failed to submit decision: {resp.text}")
        return resp.json()

    # 6. Surveillance & Detection
    def query_alerts(
        self,
        agent_id: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        params = {}
        if agent_id:
            params["agent_id"] = agent_id
        if severity:
            params["severity"] = severity
        if status:
            params["status"] = status
        resp = self._get("/alerts", params=params)
        if resp.status_code != 200:
            raise AnubisError(f"Failed to query alerts: {resp.text}")
        return resp.json()

    def verify_audit_integrity(self) -> Dict[str, Any]:
        resp = self._get("/audit/verify")
        if resp.status_code != 200:
            raise AnubisError(f"Audit verification request failed: {resp.text}")
        return resp.json()
