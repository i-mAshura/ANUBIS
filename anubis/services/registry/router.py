from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from anubis.db import get_db
from anubis.services.registry.schemas import (
    OwnerCreate, OwnerResponse,
    AgentCreate, AgentUpdate, AgentResponse, AgentRegisterResponse,
    AgentInstanceCreate, AgentInstanceResponse
)
from anubis.services.registry.service import RegistryService

router = APIRouter(tags=["Agent Registry"])


# Owners Endpoints
@router.post("/owners", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED)
def create_owner(owner_in: OwnerCreate, db: Session = Depends(get_db)):
    """Register a new human or team owner accountable for agents."""
    return RegistryService.create_owner(db, owner_in)


@router.get("/owners", response_model=List[OwnerResponse])
def list_owners(db: Session = Depends(get_db)):
    """List all registered owners."""
    return RegistryService.list_owners(db)


@router.get("/owners/{owner_id}", response_model=OwnerResponse)
def get_owner(owner_id: str, db: Session = Depends(get_db)):
    """Get owner details by ID."""
    owner = RegistryService.get_owner(db, owner_id)
    if not owner:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner


# Agents Endpoints (Section 10 API Blueprint)
@router.post("/agents", response_model=AgentRegisterResponse, status_code=status.HTTP_201_CREATED)
def register_agent(agent_in: AgentCreate, db: Session = Depends(get_db)):
    """
    Register a new AI Agent with verifiable identity.
    If no public_key is provided, an ES256 keypair will be generated automatically.
    """
    agent, priv_key = RegistryService.register_agent(db, agent_in)
    return AgentRegisterResponse(
        agent=AgentResponse.model_validate(agent),
        private_key_pem=priv_key
    )


@router.get("/agents", response_model=List[AgentResponse])
def list_agents(
    status: Optional[str] = Query(None, description="Filter by status: active, suspended, revoked"),
    db: Session = Depends(get_db)
):
    """List registered agents with optional status filtering."""
    agents = RegistryService.list_agents(db, status_filter=status)
    return [AgentResponse.model_validate(a) for a in agents]


@router.get("/agents/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """Retrieve details and public key for an agent."""
    agent = RegistryService.get_agent(db, agent_id)
    if not agent:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Agent not found")
    return AgentResponse.model_validate(agent)


@router.patch("/agents/{agent_id}", response_model=AgentResponse)
def update_agent(agent_id: str, update_in: AgentUpdate, db: Session = Depends(get_db)):
    """Update agent metadata or status (suspend, revoke, reactivate)."""
    updated = RegistryService.update_agent(db, agent_id, update_in)
    return AgentResponse.model_validate(updated)


# Agent Instances Endpoints
@router.post("/agents/{agent_id}/instances", response_model=AgentInstanceResponse, status_code=status.HTTP_201_CREATED)
def create_instance(agent_id: str, instance_in: AgentInstanceCreate, db: Session = Depends(get_db)):
    """Register a runtime instance of an agent."""
    instance_in.agent_id = agent_id
    return RegistryService.register_instance(db, instance_in)
