from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from anubis.db import get_db
from anubis.services.audit.models import AuditEvent
from anubis.services.audit.schemas import AuditEventResponse, AuditVerificationResponse
from anubis.services.audit.service import AuditService

router = APIRouter(tags=["Audit Trail"])


@router.get("/audit", response_model=List[AuditEventResponse])
def get_audit_trail(
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    tool: Optional[str] = Query(None, description="Filter by tool name"),
    decision: Optional[str] = Query(None, description="Filter by decision: allow, deny, require_approval"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Query tamper-evident audit records with optional filters and pagination."""
    events = AuditService.list_events(
        db=db,
        agent_id=agent_id,
        tool=tool,
        decision=decision,
        limit=limit,
        offset=offset
    )
    return [AuditEventResponse.model_validate(e) for e in events]


@router.get("/audit/verify", response_model=AuditVerificationResponse)
def verify_audit_trail(db: Session = Depends(get_db)):
    """
    Cryptographic verification endpoint.
    Recalculates SHA-256 hash chains across all records from Genesis to detect any tampering or deletion.
    """
    return AuditService.verify_chain(db)


@router.get("/audit/{event_id}", response_model=AuditEventResponse)
def get_audit_event(event_id: str, db: Session = Depends(get_db)):
    """Retrieve details for a specific audit record."""
    event = db.query(AuditEvent).filter(AuditEvent.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit event '{event_id}' not found."
        )
    return AuditEventResponse.model_validate(event)
