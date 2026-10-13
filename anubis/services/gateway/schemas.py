from datetime import datetime
from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, ConfigDict, Field


class ToolCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    server: str = Field(..., min_length=2, max_length=120)
    description: Optional[str] = None
    risk_level: str = "low"  # low, medium, high, critical
    required_scope: str = "tools:read"
    argument_schema: Optional[Dict[str, Any]] = None
    downstream_credential_ref: Optional[str] = None
    downstream_secret_value: Optional[str] = None  # Secret stored in vault


class ToolResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    server: str
    description: Optional[str] = None
    risk_level: str
    required_scope: str
    argument_schema: Optional[Dict[str, Any]] = None
    downstream_credential_ref: Optional[str] = None
    created_at: datetime
    # Note: downstream_secret_value is deliberately excluded to prevent secret leakage!


# Model Context Protocol (MCP) JSON-RPC 2.0 schemas
class MCPCallParams(BaseModel):
    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = 1
    method: str = "tools/call"  # tools/call or tools/list
    params: Optional[Union[MCPCallParams, Dict[str, Any]]] = None


class MCPError(BaseModel):
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None


class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = 1
    result: Optional[Dict[str, Any]] = None
    error: Optional[MCPError] = None
