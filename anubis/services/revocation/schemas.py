from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class RevocationCreate(BaseModel):
    target_type: str = Field(..., pattern=r"^(agent|instance|task|token|principal)$")
    target_id: str = Field(..., min_length=2, max_length=120)
    reason: str = Field(..., min_length=3)
    revoked_by: Optional[str] = "admin"


class RevocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    target_type: str
    target_id: str
    reason: str
    revoked_by: str
    revoked_at: datetime
    active: bool
