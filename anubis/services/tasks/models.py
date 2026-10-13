import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from anubis.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=lambda: f"task_{uuid.uuid4().hex[:12]}")
    root_agent_id = Column(String(64), ForeignKey("agents.id"), nullable=False, index=True)
    on_behalf_of = Column(String(120), nullable=False, index=True)  # Human principal or service identity
    intent = Column(Text, nullable=False)  # Description / goal of the autonomous task
    requested_scope = Column(JSON, nullable=True)  # Allowed scopes for this overall task
    status = Column(String(50), default="running", nullable=False)  # running, completed, failed, cancelled
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    agent = relationship("Agent")
