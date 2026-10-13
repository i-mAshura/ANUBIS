import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON
from anubis.db import Base


class Tool(Base):
    __tablename__ = "tools"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(120), nullable=False, unique=True, index=True)
    server = Column(String(120), nullable=False, index=True)
    description = Column(Text, nullable=True)
    risk_level = Column(String(50), default="low", nullable=False)  # low, medium, high, critical
    required_scope = Column(String(100), default="tools:read", nullable=False)
    argument_schema = Column(JSON, nullable=True)
    downstream_credential_ref = Column(String(120), nullable=True)
    downstream_secret_value = Column(Text, nullable=True)  # Secret held by gateway, never shown to agent
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
