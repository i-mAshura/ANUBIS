import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from anubis.db import get_db
from anubis.services.policy.models import Policy
from anubis.services.policy.schemas import (
    PolicyCreate, PolicyResponse, PolicyEvaluationInput, PolicyDecisionResponse
)
from anubis.services.policy.evaluator import policy_evaluator

router = APIRouter(tags=["Policy Engine"])


@router.post("/policies", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
def create_policy(policy_in: PolicyCreate, db: Session = Depends(get_db)):
    """Register or update a declarative OPA Rego policy."""
    existing = db.query(Policy).filter(Policy.name == policy_in.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Policy with name '{policy_in.name}' already exists."
        )

    policy = Policy(
        id=str(uuid.uuid4()),
        name=policy_in.name,
        version=policy_in.version,
        description=policy_in.description,
        rego_source=policy_in.rego_source,
        status=policy_in.status,
        created_by="admin",
        created_at=datetime.utcnow()
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return PolicyResponse.model_validate(policy)


@router.get("/policies", response_model=List[PolicyResponse])
def list_policies(db: Session = Depends(get_db)):
    """List all registered access control policies."""
    policies = db.query(Policy).all()
    return [PolicyResponse.model_validate(p) for p in policies]


@router.post("/policies/simulate", response_model=PolicyDecisionResponse)
async def simulate_policy(eval_input: PolicyEvaluationInput):
    """
    Simulate and test policy decisions (allow, deny, require_approval) against input context.
    """
    return await policy_evaluator.evaluate(eval_input)
