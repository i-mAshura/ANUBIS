from typing import Optional, Dict, Any, List
from anubis.sdk.client import AnubisClient
from anubis.sdk.exceptions import AnubisApprovalRequiredError, AnubisPolicyDeniedError, AnubisKillSwitchError


class AnubisAgent:
    """
    High-level autonomous agent wrapper.
    Automates identity bootstrapping, credential isolation, delegated sub-agent spawning,
    and mediated MCP tool execution under ANUBIS zero-trust governance.
    """

    def __init__(
        self,
        name: str,
        owner_id: str,
        purpose: str,
        risk_tier: str = "low",
        capabilities: Optional[List[str]] = None,
        base_url: str = "http://localhost:8000",
        client: Optional[AnubisClient] = None
    ):
        self.name = name
        self.owner_id = owner_id
        self.purpose = purpose
        self.risk_tier = risk_tier
        self.capabilities = capabilities or []
        self.client = client or AnubisClient(base_url=base_url)
        self.agent_id: Optional[str] = None
        self.active_task_id: Optional[str] = None

    def bootstrap(self, scope: Optional[List[str]] = None) -> str:
        """
        Registers this agent with the ANUBIS control plane (deriving its cryptographic ID)
        and performs challenge-response authentication.
        """
        reg_data = self.client.register_agent(
            name=self.name,
            owner_id=self.owner_id,
            purpose=self.purpose,
            risk_tier=self.risk_tier,
            capabilities=self.capabilities,
            generate_local_key=True
        )
        self.agent_id = self.client.agent_id
        token = self.client.authenticate(scope=scope, task_id=self.active_task_id)
        return token

    def execute_tool(
        self,
        server: str,
        tool_name: str,
        arguments: Optional[Dict[str, Any]] = None,
        approval_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Invokes an MCP tool through the ANUBIS Gateway.
        """
        return self.client.invoke_tool(
            server=server,
            tool_name=tool_name,
            arguments=arguments,
            approval_id=approval_id
        )

    def spawn_subagent(
        self,
        name: str,
        purpose: str,
        task_intent: str,
        delegated_scope: List[str],
        risk_tier: str = "low",
        on_behalf_of: Optional[str] = None
    ) -> "AnubisAgent":
        """
        Spawns a child autonomous sub-agent with a task and delegated token.
        Enforces monotonic scope narrowing and cryptographic audit trail lineage.
        """
        # 1. Create task record
        task_data = self.client.create_task(
            intent=task_intent,
            on_behalf_of=on_behalf_of or "system",
            root_agent_id=self.agent_id,
            requested_scope=delegated_scope
        )
        sub_task_id = task_data["id"]

        # 2. Register child agent
        child_client = AnubisClient(
            base_url=self.client.base_url,
            http_client=self.client._http
        )
        child_client.register_agent(
            name=name,
            owner_id=self.owner_id,
            purpose=purpose,
            risk_tier=risk_tier,
            capabilities=delegated_scope,
            generate_local_key=True
        )

        # 3. Exchange current token for delegated token
        exchange_data = self.client.delegate_token(
            target_agent_id=child_client.agent_id,
            task_id=sub_task_id,
            requested_scope=delegated_scope
        )
        child_client.access_token = exchange_data["access_token"]

        # 4. Return initialized child agent
        child_agent = AnubisAgent(
            name=name,
            owner_id=self.owner_id,
            purpose=purpose,
            risk_tier=risk_tier,
            capabilities=delegated_scope,
            client=child_client
        )
        child_agent.agent_id = child_client.agent_id
        child_agent.active_task_id = sub_task_id
        return child_agent
