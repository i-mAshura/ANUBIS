import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from anubis.db import Base, get_db
# Import all models to ensure they are registered with Base.metadata
from anubis.services.registry.models import Owner, Agent, AgentInstance
from anubis.services.policy.models import Policy
from anubis.services.gateway.models import Tool
from anubis.services.audit.models import AuditEvent
from anubis.services.tasks.models import Task
from anubis.services.approvals.models import ApprovalRequest
from anubis.services.revocation.models import RevocationEntry
from anubis.services.detection.models import Alert, AgentBaseline
from anubis.main import app

# In-memory SQLite with StaticPool so all connections share the same memory DB
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


from anubis.services.revocation.service import RevocationService
from anubis.services.detection.engine import DetectionEngine
from anubis.services.gateway.service import _revoked_entities


@pytest.fixture(scope="function", autouse=True)
def db_session():
    RevocationService.clear_cache()
    DetectionEngine.clear_buffers()
    _revoked_entities.clear()
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        RevocationService.clear_cache()
        DetectionEngine.clear_buffers()
        _revoked_entities.clear()


@pytest.fixture(scope="function")
def client():
    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
