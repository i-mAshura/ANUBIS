from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    root_agent_id: str
    on_behalf_of: str = Field(..., min_length=2, max_length=120)
    intent: str = Field(..., min_length=5)
    requested_scope: Optional[List[str]] = Field(default_factory=lambda: ["tools:read"])


class TaskUpdate(BaseModel):
    status: Optional[str] = None  # completed, failed, cancelled


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    root_agent_id: str
    on_behalf_of: str
    intent: str
    requested_scope: Optional[List[str]] = None
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
