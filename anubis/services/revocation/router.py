from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from anubis.db import get_db
from anubis.services.revocation.schemas import RevocationCreate, RevocationResponse
from anubis.services.revocation.service import RevocationService

router = APIRouter(tags=["Revocation & Kill Switch"])


@router.post("/revocations", response_model=RevocationResponse, status_code=status.HTTP_201_CREATED)
def trigger_kill_switch(rev_in: RevocationCreate, db: Session = Depends(get_db)):
    """
    Trigger instant kill switch to revoke an agent, instance, task, token, or human principal.
    Takes effect immediately across the gateway.
    """
    return RevocationService.revoke(db, rev_in)


@router.get("/revocations", response_model=List[RevocationResponse])
def list_revocations(
    active_only: bool = Query(True, description="Filter for active revocations only"),
    db: Session = Depends(get_db)
):
    """List all active or past revocation records."""
    return RevocationService.list_revocations(db, active_only=active_only)


@router.delete("/revocations/{rev_id}", response_model=RevocationResponse)
def restore_revocation(rev_id: str, db: Session = Depends(get_db)):
    """Deactivate a revocation entry, restoring access."""
    return RevocationService.deactivate_revocation(db, rev_id)
