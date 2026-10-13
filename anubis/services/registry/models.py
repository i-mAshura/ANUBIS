import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from anubis.db import Base


class Owner(Base):
    __tablename__ = "owners"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    team = Column(String(120), nullable=True)
    external_idp_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    agents = relationship("Agent", back_populates="owner", cascade="all, delete-orphan")


class Agent(Base):
    __tablename__ = "agents"

    id = Column(String(64), primary_key=True)
    name = Column(String(120), nullable=False, index=True)
    owner_id = Column(String(36), ForeignKey("owners.id"), nullable=False, index=True)
    purpose = Column(Text, nullable=False)
    framework = Column(String(100), default="custom", nullable=False)  # langchain, crewai, claude-sdk, etc.
    environment = Column(String(50), default="development", nullable=False)  # dev, staging, prod
    risk_tier = Column(String(50), default="low", nullable=False)  # low, medium, high, critical
    public_key = Column(Text, nullable=False)  # PEM format public key
    status = Column(String(50), default="active", nullable=False)  # active, suspended, revoked
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)

    owner = relationship("Owner", back_populates="agents")
    instances = relationship("AgentInstance", back_populates="agent", cascade="all, delete-orphan")


class AgentInstance(Base):
    __tablename__ = "agent_instances"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String(64), ForeignKey("agents.id"), nullable=False, index=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    runtime_info = Column(JSON, nullable=True)
    attestation = Column(Text, nullable=True)

    agent = relationship("Agent", back_populates="instances")
