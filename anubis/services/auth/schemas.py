from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChallengeRequest(BaseModel):
    agent_id: str
    instance_id: Optional[str] = None


class ChallengeResponse(BaseModel):
    challenge_id: str
    agent_id: str
    challenge: str
    expires_at: datetime


class TokenRequest(BaseModel):
    agent_id: str
    instance_id: str
    challenge_id: str
    signature: str  # URL-safe Base64 signature of the challenge string
    task_id: Optional[str] = "task-default"
    on_behalf_of: Optional[str] = "system"
    requested_scope: Optional[List[str]] = Field(default_factory=lambda: ["tools:read"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    jti: str
    claims: Dict[str, Any]


class KeypairGenerateResponse(BaseModel):
    public_key_pem: str
    private_key_pem: str
    curve: str = "secp256r1 (P-256)"
    algorithm: str = "ES256"
