import uuid
from datetime import datetime, timedelta
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey
from anubis.db import Base


class ApprovalRequest(Base):
    __tablename__ = "approvals"

    id = Column(String(36), primary_key=True, default=lambda: f"appr_{uuid.uuid4().hex[:12]}")
    trace_id = Column(String(64), nullable=False, index=True)
    audit_event_id = Column(String(36), nullable=True)
    agent_id = Column(String(64), ForeignKey("agents.id"), nullable=False, index=True)
    task_id = Column(String(64), nullable=True, index=True)
    tool = Column(String(120), nullable=False, index=True)
    arguments = Column(JSON, nullable=True)
    reason = Column(Text, nullable=False)
    status = Column(String(50), default="pending", nullable=False, index=True)  # pending, approved, rejected, expired, consumed
    approver_id = Column(String(120), nullable=True)
    decision = Column(String(50), nullable=True)  # approved, rejected
    decision_comment = Column(Text, nullable=True)
    requested_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    decided_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=30), nullable=False)
