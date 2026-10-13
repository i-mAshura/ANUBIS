import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from anubis.db import Base


class Policy(Base):
    __tablename__ = "policies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(120), nullable=False, unique=True, index=True)
    version = Column(String(50), default="1.0.0", nullable=False)
    description = Column(Text, nullable=True)
    rego_source = Column(Text, nullable=False)
    status = Column(String(50), default="active", nullable=False)  # active, disabled
    created_by = Column(String(120), default="admin", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
