import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON, Integer, Float, ForeignKey
from anubis.db import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String(36), primary_key=True, default=lambda: f"alt_{uuid.uuid4().hex[:12]}")
    agent_id = Column(String(64), ForeignKey("agents.id"), nullable=False, index=True)
    rule = Column(String(100), nullable=False, index=True)  # denial_burst, novel_tool_probe, volume_spike, off_hours_activity
    severity = Column(String(50), default="medium", nullable=False)  # low, medium, high, critical
    details = Column(JSON, nullable=True)
    action_taken = Column(String(50), default="alert", nullable=False)  # alert, require_approval, suspend, revoke
    status = Column(String(50), default="active", nullable=False, index=True)  # active, acknowledged, resolved
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class AgentBaseline(Base):
    __tablename__ = "agent_baselines"

    id = Column(String(36), primary_key=True, default=lambda: f"base_{uuid.uuid4().hex[:12]}")
    agent_id = Column(String(64), ForeignKey("agents.id"), unique=True, nullable=False, index=True)
    known_tools = Column(JSON, default=list, nullable=False)
    total_calls = Column(Integer, default=0, nullable=False)
    total_denials = Column(Integer, default=0, nullable=False)
    last_seen_at = Column(DateTime, default=datetime.utcnow, nullable=False)
