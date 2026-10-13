import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Boolean
from anubis.db import Base


class RevocationEntry(Base):
    __tablename__ = "revocations"

    id = Column(String(36), primary_key=True, default=lambda: f"rev_{uuid.uuid4().hex[:12]}")
    target_type = Column(String(50), nullable=False, index=True)  # agent, instance, task, token, principal
    target_id = Column(String(120), nullable=False, index=True)
    reason = Column(Text, nullable=False)
    revoked_by = Column(String(120), default="system", nullable=False)
    revoked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
