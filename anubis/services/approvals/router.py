from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from anubis.db import get_db
from anubis.services.approvals.schemas import ApprovalResponse, ApprovalDecisionRequest
from anubis.services.approvals.service import ApprovalService

router = APIRouter(tags=["Approvals Queue"])


@router.get("/approvals", response_model=List[ApprovalResponse])
def list_approvals(
    status: Optional[str] = Query(None, description="Filter by status: pending, approved, rejected, expired, consumed"),
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    db: Session = Depends(get_db)
):
    """List pending and historical human-in-the-loop approval requests."""
    return ApprovalService.list_approvals(db, status_filter=status, agent_id=agent_id)


@router.get("/approvals/{approval_id}", response_model=ApprovalResponse)
def get_approval(approval_id: str, db: Session = Depends(get_db)):
    """Retrieve details for a specific approval request."""
    approval = ApprovalService.get_approval(db, approval_id)
    if not approval:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval request not found.")
    return ApprovalResponse.model_validate(approval)


@router.post("/approvals/{approval_id}/decision", response_model=ApprovalResponse)
def decide_approval(
    approval_id: str,
    decision_in: ApprovalDecisionRequest,
    db: Session = Depends(get_db)
):
    """
    Decide a pending approval request (approve or reject).
    Decisions are recorded into the tamper-evident audit trail and are single-use.
    """
    return ApprovalService.decide_approval(db, approval_id, decision_in)
