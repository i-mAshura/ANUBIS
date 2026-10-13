from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict, Field


class ApprovalDecisionRequest(BaseModel):
    decision: str = Field(..., pattern=r"^(approved|rejected)$")
    approver_id: str = Field(..., min_length=2, max_length=120)
    comment: Optional[str] = None


class ApprovalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    trace_id: str
    audit_event_id: Optional[str] = None
    agent_id: str
    task_id: Optional[str] = None
    tool: str
    arguments: Optional[Dict[str, Any]] = None
    reason: str
    status: str
    approver_id: Optional[str] = None
    decision: Optional[str] = None
    decision_comment: Optional[str] = None
    requested_at: datetime
    decided_at: Optional[datetime] = None
    expires_at: datetime
