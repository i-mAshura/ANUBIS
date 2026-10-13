import uuid
import time
import jwt
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from anubis.services.auth.service import token_service
from anubis.services.registry.models import Agent
from anubis.services.gateway.models import Tool
from anubis.services.audit.service import AuditService
from anubis.services.gateway.schemas import (
    MCPRequest, MCPResponse, MCPError, MCPCallParams, ToolCreate
)
from anubis.services.policy.schemas import (
    PolicyEvaluationInput, AgentContext, TokenContext, ActionContext
)
from anubis.services.policy.evaluator import policy_evaluator
from anubis.services.gateway.credential_broker import credential_broker
from anubis.services.gateway.mock_mcp import MockMCPServer

# In-memory revocation set (will be synchronized with Redis in distributed deployments)
_revoked_entities = set()


def revoke_entity(entity_id: str):
    """Blacklists an agent_id, instance_id, or token jti."""
    _revoked_entities.add(entity_id)


def is_revoked(entity_id: str) -> bool:
    return entity_id in _revoked_entities


class GatewayService:
    @staticmethod
    def register_tool(db: Session, tool_in: ToolCreate) -> Tool:
        existing = db.query(Tool).filter(Tool.name == tool_in.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tool with name '{tool_in.name}' already registered."
            )
        tool = Tool(
            id=str(uuid.uuid4()),
            name=tool_in.name,
            server=tool_in.server,
            description=tool_in.description,
            risk_level=tool_in.risk_level,
            required_scope=tool_in.required_scope,
            argument_schema=tool_in.argument_schema,
            downstream_credential_ref=tool_in.downstream_credential_ref,
            downstream_secret_value=tool_in.downstream_secret_value
        )
        db.add(tool)
        db.commit()
        db.refresh(tool)
        return tool

    @staticmethod
    async def process_mcp_request(
        db: Session,
        server: str,
        token_str: str,
        mcp_req: MCPRequest
    ) -> MCPResponse:
        req_id = mcp_req.id or 1

        # 1. Validate Token (signature, expiration, issuer, claims)
        try:
            claims = token_service.verify_token(token_str)
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired. Re-authenticate via /auth/challenge."
            )
        except jwt.PyJWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token signature or format: {str(e)}"
            )

        agent_id = claims.get("sub")
        instance_id = claims.get("instance_id")
        jti = claims.get("jti")
        token_scopes = claims.get("scope", [])

        # 2. Revocation Check (Kill switch)
        if is_revoked(agent_id) or is_revoked(instance_id) or is_revoked(jti):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Agent or Token has been revoked by kill switch."
            )

        # 3. Agent Existence & Status Check in Registry
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent '{agent_id}' does not exist in registry."
            )
        if agent.status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Agent '{agent_id}' is '{agent.status}'. Execution blocked."
            )

        # 4. Handle MCP Method
        if mcp_req.method == "tools/list":
            tools = db.query(Tool).filter(Tool.server == server).all()
            return MCPResponse(
                id=req_id,
                result={
                    "tools": [
                        {
                            "name": t.name,
                            "description": t.description,
                            "inputSchema": t.argument_schema or {"type": "object"}
                        }
                        for t in tools
                    ]
                }
            )

        if mcp_req.method != "tools/call":
            return MCPResponse(
                id=req_id,
                error=MCPError(
                    code=-32601,
                    message=f"Unsupported MCP method: '{mcp_req.method}'."
                )
            )

        # Parse tool name and arguments from params
        tool_name = ""
        arguments = {}
        if isinstance(mcp_req.params, MCPCallParams):
            tool_name = mcp_req.params.name
            arguments = mcp_req.params.arguments
        elif isinstance(mcp_req.params, dict):
            tool_name = mcp_req.params.get("name", "")
            arguments = mcp_req.params.get("arguments", {})

        if not tool_name:
            return MCPResponse(
                id=req_id,
                error=MCPError(code=-32602, message="Missing required parameter: tool 'name'")
            )

        # 5. Policy Engine Evaluation (Fail-Closed)
        start_time = time.time()
        trace_id = str(uuid.uuid4())
        task_id = claims.get("task_id", "task-default")
        delegation_chain = claims.get("act", [agent.id])

        eval_input = PolicyEvaluationInput(
            agent=AgentContext(
                id=agent.id,
                name=agent.name,
                risk_tier=agent.risk_tier,
                owner_id=agent.owner_id
            ),
            token=TokenContext(
                sub=claims["sub"],
                instance_id=claims.get("instance_id"),
                scope=token_scopes,
                task_id=task_id,
                act=delegation_chain
            ),
            action=ActionContext(
                tool=tool_name,
                server=server,
                arguments=arguments
            )
        )

        try:
            decision_response = await policy_evaluator.evaluate(eval_input)
        except Exception as exc:
            # Absolute Fail-Closed invariant on policy error/outage
            latency_ms = (time.time() - start_time) * 1000
            AuditService.record_event(
                db=db,
                trace_id=trace_id,
                agent_id=agent.id,
                tool=tool_name,
                decision="deny",
                outcome="error",
                task_id=task_id,
                instance_id=instance_id,
                chain=delegation_chain,
                arguments=arguments,
                reason=f"Policy evaluation failure: {str(exc)}",
                latency_ms=latency_ms
            )
            return MCPResponse(
                id=req_id,
                error=MCPError(
                    code=-32003,
                    message=f"Access Denied: Policy evaluation failed ({str(exc)}) - Fail-Closed enforced."
                )
            )

        latency_ms = (time.time() - start_time) * 1000

        if decision_response.decision == "deny":
            AuditService.record_event(
                db=db,
                trace_id=trace_id,
                agent_id=agent.id,
                tool=tool_name,
                decision="deny",
                outcome="denied",
                task_id=task_id,
                instance_id=instance_id,
                chain=delegation_chain,
                arguments=arguments,
                reason=decision_response.reason,
                latency_ms=latency_ms
            )
            return MCPResponse(
                id=req_id,
                error=MCPError(
                    code=-32003,
                    message=f"Access Denied by Policy: {decision_response.reason}"
                )
            )

        if decision_response.decision == "require_approval":
            approval_id = str(uuid.uuid4())
            AuditService.record_event(
                db=db,
                trace_id=trace_id,
                agent_id=agent.id,
                tool=tool_name,
                decision="require_approval",
                outcome="pending_approval",
                task_id=task_id,
                instance_id=instance_id,
                chain=delegation_chain,
                arguments=arguments,
                reason=decision_response.reason,
                latency_ms=latency_ms
            )
            return MCPResponse(
                id=req_id,
                result={
                    "status": "pending_approval",
                    "approval_id": approval_id,
                    "message": f"Action paused for human review: {decision_response.reason}",
                    "tool": tool_name
                }
            )

        # 6. Credential Brokering: Retrieve downstream secrets (agent never sees them)
        brokered_secret = credential_broker.get_credential_for_tool(db, tool_name)

        # 7. Forward call to downstream / mock MCP server
        raw_result = MockMCPServer.execute_tool(
            server=server,
            tool_name=tool_name,
            arguments=arguments,
            brokered_credential=brokered_secret
        )

        # 8. Record audit event for allowed and executed tool call
        AuditService.record_event(
            db=db,
            trace_id=trace_id,
            agent_id=agent.id,
            tool=tool_name,
            decision="allow",
            outcome="success",
            task_id=task_id,
            instance_id=instance_id,
            chain=delegation_chain,
            arguments=arguments,
            reason=decision_response.reason,
            latency_ms=latency_ms
        )

        # 9. Sanitize & redact any secrets from the outgoing result
        sanitized_result = credential_broker.redact_secrets(raw_result)

        return MCPResponse(
            id=req_id,
            result=sanitized_result
        )
