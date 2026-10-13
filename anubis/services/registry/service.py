import uuid
from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from anubis.services.registry.models import Agent, Owner, AgentInstance
from anubis.services.registry.schemas import (
    AgentCreate, AgentUpdate, OwnerCreate, AgentInstanceCreate
)
from anubis.services.auth.crypto import generate_es256_keypair, derive_cryptographic_agent_id


class RegistryService:
    @staticmethod
    def create_owner(db: Session, owner_in: OwnerCreate) -> Owner:
        existing = db.query(Owner).filter(Owner.email == owner_in.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Owner with email '{owner_in.email}' already exists."
            )
        owner = Owner(
            id=str(uuid.uuid4()),
            name=owner_in.name,
            email=owner_in.email,
            team=owner_in.team,
            external_idp_id=owner_in.external_idp_id,
            created_at=datetime.utcnow()
        )
        db.add(owner)
        db.commit()
        db.refresh(owner)
        return owner

    @staticmethod
    def get_owner(db: Session, owner_id: str) -> Optional[Owner]:
        return db.query(Owner).filter(Owner.id == owner_id).first()

    @staticmethod
    def list_owners(db: Session) -> List[Owner]:
        return db.query(Owner).all()

    @staticmethod
    def register_agent(db: Session, agent_in: AgentCreate) -> Tuple[Agent, Optional[str]]:
        owner = db.query(Owner).filter(Owner.id == agent_in.owner_id).first()
        if not owner:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Owner ID '{agent_in.owner_id}' not found. Agents must have a registered owner."
            )

        generated_private_key = None
        public_key = agent_in.public_key

        if not public_key:
            # Auto-generate ES256 keypair if not supplied
            generated_private_key, public_key = generate_es256_keypair()

        # Cryptographic unique identity derived atomically from public key SubjectPublicKeyInfo fingerprint
        cryptographic_agent_id = derive_cryptographic_agent_id(public_key)

        agent = Agent(
            id=cryptographic_agent_id,
            name=agent_in.name,
            owner_id=agent_in.owner_id,
            purpose=agent_in.purpose,
            framework=agent_in.framework,
            environment=agent_in.environment,
            risk_tier=agent_in.risk_tier,
            public_key=public_key,
            status="active",
            created_at=datetime.utcnow(),
            expires_at=agent_in.expires_at
        )
        db.add(agent)
        db.commit()
        db.refresh(agent)
        return agent, generated_private_key

    @staticmethod
    def get_agent(db: Session, agent_id: str) -> Optional[Agent]:
        return db.query(Agent).filter(Agent.id == agent_id).first()

    @staticmethod
    def list_agents(db: Session, status_filter: Optional[str] = None) -> List[Agent]:
        query = db.query(Agent)
        if status_filter:
            query = query.filter(Agent.status == status_filter)
        return query.all()

    @staticmethod
    def update_agent(db: Session, agent_id: str, update_in: AgentUpdate) -> Agent:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

        update_data = update_in.model_dump(exclude_unset=True)
        for key, val in update_data.items():
            setattr(agent, key, val)

        db.commit()
        db.refresh(agent)
        return agent

    @staticmethod
    def suspend_agent(db: Session, agent_id: str) -> Agent:
        return RegistryService.update_agent(db, agent_id, AgentUpdate(status="suspended"))

    @staticmethod
    def revoke_agent(db: Session, agent_id: str) -> Agent:
        return RegistryService.update_agent(db, agent_id, AgentUpdate(status="revoked"))

    @staticmethod
    def register_instance(db: Session, instance_in: AgentInstanceCreate) -> AgentInstance:
        agent = db.query(Agent).filter(Agent.id == instance_in.agent_id).first()
        if not agent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
        if agent.status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Cannot start instance for agent with status '{agent.status}'"
            )

        instance = AgentInstance(
            id=str(uuid.uuid4()),
            agent_id=instance_in.agent_id,
            started_at=datetime.utcnow(),
            runtime_info=instance_in.runtime_info,
            attestation=instance_in.attestation
        )
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance
