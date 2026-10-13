from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from anubis.config import settings
from anubis.db import init_db
from anubis.services.registry.router import router as registry_router
from anubis.services.auth.router import router as auth_router
from anubis.services.policy.router import router as policy_router
from anubis.services.gateway.router import router as gateway_router
from anubis.services.audit.router import router as audit_router
from anubis.services.auth.service import AuthService
# Import models to ensure they are registered with Base metadata
from anubis.services.registry.models import Owner, Agent, AgentInstance
from anubis.services.policy.models import Policy
from anubis.services.gateway.models import Tool
from anubis.services.audit.models import AuditEvent


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize tables
    init_db()
    yield
    # Shutdown logic (if any)


app = FastAPI(
    title="ANUBIS Control Plane",
    description="Identity, IAM, and Tracking Control Plane for Autonomous AI Agents",
    version=settings.VERSION,
    lifespan=lifespan
)

# Enable CORS for dashboard and local tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Service Routers
app.include_router(registry_router)
app.include_router(auth_router)
app.include_router(policy_router)
app.include_router(gateway_router)
app.include_router(audit_router)


@app.get("/.well-known/jwks.json", tags=["JWKS"])
def get_jwks():
    """
    Standard RFC 7517 JSON Web Key Set (JWKS) endpoint publishing ANUBIS active public keys.
    """
    return AuthService.get_jwks()


@app.get("/health", tags=["System"])
def health_check():
    """System liveness check."""
    return {
        "status": "healthy",
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ANUBIS_ENV
    }


@app.get("/", tags=["System"])
def root():
    return {
        "project": "ANUBIS",
        "tagline": "Every agent is weighed before it passes, and the record never lies.",
        "docs_url": "/docs",
        "jwks_url": "/.well-known/jwks.json"
    }
