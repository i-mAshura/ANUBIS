from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, ConfigDict, Field


# Owners
class OwnerCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: str = Field(..., pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    team: Optional[str] = None
    external_idp_id: Optional[str] = None


class OwnerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str
    team: Optional[str] = None
    external_idp_id: Optional[str] = None
    created_at: datetime


# Agents
class AgentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    owner_id: str
    purpose: str = Field(..., min_length=5)
    framework: str = "custom"
    environment: str = "development"
    risk_tier: str = "low"  # low, medium, high, critical
    public_key: Optional[str] = None  # If not provided, server can generate a keypair
    expires_at: Optional[datetime] = None


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    purpose: Optional[str] = None
    status: Optional[str] = None  # active, suspended, revoked
    risk_tier: Optional[str] = None
    expires_at: Optional[datetime] = None


class AgentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    owner_id: str
    purpose: str
    framework: str
    environment: str
    risk_tier: str
    public_key: str
    status: str
    created_at: datetime
    expires_at: Optional[datetime] = None


class AgentRegisterResponse(BaseModel):
    agent: AgentResponse
    private_key_pem: Optional[str] = None  # Returned ONLY if server generated the keypair upon registration


# Instances
class AgentInstanceCreate(BaseModel):
    agent_id: str
    runtime_info: Optional[Dict[str, Any]] = None
    attestation: Optional[str] = None


class AgentInstanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    agent_id: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    runtime_info: Optional[Dict[str, Any]] = None
    attestation: Optional[str] = None
