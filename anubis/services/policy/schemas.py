from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict, Field


class PolicyCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    version: str = "1.0.0"
    description: Optional[str] = None
    rego_source: str = Field(..., min_length=5)
    status: str = "active"


class PolicyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    version: str
    description: Optional[str] = None
    rego_source: str
    status: str
    created_by: str
    created_at: datetime


class AgentContext(BaseModel):
    id: str
    name: Optional[str] = "unknown"
    risk_tier: str = "low"
    owner_id: Optional[str] = None


class TokenContext(BaseModel):
    sub: str
    instance_id: Optional[str] = None
    scope: List[str] = Field(default_factory=list)
    task_id: Optional[str] = None
    act: Optional[List[str]] = Field(default_factory=list)


class ActionContext(BaseModel):
    tool: str
    server: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class PolicyEvaluationInput(BaseModel):
    agent: AgentContext
    token: TokenContext
    action: ActionContext


class PolicyDecisionResponse(BaseModel):
    decision: str  # allow, deny, require_approval
    reason: str
    rule_matched: Optional[str] = None
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)
