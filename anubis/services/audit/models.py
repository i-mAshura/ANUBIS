import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, Float
from anubis.db import Base


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    seq = Column(Integer, unique=True, index=True, nullable=False)
    prev_hash = Column(String(64), nullable=False)
    hash = Column(String(64), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    trace_id = Column(String(64), nullable=False, index=True)
    task_id = Column(String(64), nullable=True)
    agent_id = Column(String(64), nullable=False, index=True)
    instance_id = Column(String(64), nullable=True)
    chain = Column(JSON, nullable=True)  # Delegation lineage list
    tool = Column(String(120), nullable=False, index=True)
    args_redacted = Column(JSON, nullable=True)
    decision = Column(String(50), nullable=False)  # allow, deny, require_approval
    reason = Column(Text, nullable=True)
    outcome = Column(String(50), nullable=False)  # success, denied, pending_approval, error
    latency_ms = Column(Float, default=0.0, nullable=False)
