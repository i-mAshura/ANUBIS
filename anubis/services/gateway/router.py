from typing import List, Optional
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from anubis.db import get_db
from anubis.services.gateway.models import Tool
from anubis.services.gateway.schemas import (
    ToolCreate, ToolResponse, MCPRequest, MCPResponse
)
from anubis.services.gateway.service import GatewayService

router = APIRouter(tags=["Gateway & MCP Proxy"])


def extract_bearer_token(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header. Expected 'Bearer <token>'."
        )
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected 'Bearer <token>'."
        )
    return parts[1]


# Tools Management
@router.post("/tools", response_model=ToolResponse, status_code=status.HTTP_201_CREATED)
def register_tool(tool_in: ToolCreate, db: Session = Depends(get_db)):
    """Register a tool with its required scope, risk level, and downstream credential reference."""
    return GatewayService.register_tool(db, tool_in)


@router.get("/tools", response_model=List[ToolResponse])
def list_tools(db: Session = Depends(get_db)):
    """List all registered tools."""
    tools = db.query(Tool).all()
    return [ToolResponse.model_validate(t) for t in tools]


# Gateway / MCP Proxy Endpoint (Section 10 API Blueprint)
@router.post("/mcp/{server}", response_model=MCPResponse)
async def proxy_mcp_call(
    server: str,
    mcp_request: MCPRequest,
    token: str = Depends(extract_bearer_token),
    db: Session = Depends(get_db)
):
    """
    Enforcement Gateway: Intercepts MCP (Model Context Protocol) tool execution requests.
    Validates token, evaluates OPA/Rego policies, brokers downstream credentials,
    and returns sanitized results.
    """
    response = await GatewayService.process_mcp_request(
        db=db,
        server=server,
        token_str=token,
        mcp_req=mcp_request
    )

    # If policy engine denied the action, map to 403 Forbidden
    if response.error and response.error.code == -32003:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=response.error.message
        )

    return response
