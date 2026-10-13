from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict, Field


class AlertUpdate(BaseModel):
    status: str = Field(..., pattern=r"^(active|acknowledged|resolved)$")


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    agent_id: str
    rule: str
    severity: str
    details: Optional[Dict[str, Any]] = None
    action_taken: str
    status: str
    created_at: datetime


class BaselineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    agent_id: str
    known_tools: List[str]
    total_calls: int
    total_denials: int
    last_seen_at: datetime
