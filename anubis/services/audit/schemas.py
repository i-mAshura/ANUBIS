from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict, Field


class AuditEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    seq: int
    prev_hash: str
    hash: str
    timestamp: datetime
    trace_id: str
    task_id: Optional[str] = None
    agent_id: str
    instance_id: Optional[str] = None
    chain: Optional[List[str]] = None
    tool: str
    args_redacted: Optional[Dict[str, Any]] = None
    decision: str
    reason: Optional[str] = None
    outcome: str
    latency_ms: float


class AuditVerificationResponse(BaseModel):
    verified: bool
    total_records: int
    latest_seq: Optional[int] = None
    latest_hash: Optional[str] = None
    genesis_hash: Optional[str] = None
    broken_at_seq: Optional[int] = None
    reason: Optional[str] = None
    verified_at: datetime = Field(default_factory=datetime.utcnow)
