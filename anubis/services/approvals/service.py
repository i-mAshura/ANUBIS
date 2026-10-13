import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from anubis.services.approvals.models import ApprovalRequest
from anubis.services.approvals.schemas import ApprovalDecisionRequest
from anubis.services.audit.service import AuditService


class ApprovalService:
    @staticmethod
    def create_approval_request(
        db: Session,
        trace_id: str,
        agent_id: str,
        tool: str,
        reason: str,
        arguments: Optional[Dict[str, Any]] = None,
        task_id: Optional[str] = None,
        ttl_minutes: int = 30
    ) -> ApprovalRequest:
        approval = ApprovalRequest(
            id=f"appr_{uuid.uuid4().hex[:12]}",
            trace_id=trace_id,
            agent_id=agent_id,
            task_id=task_id,
            tool=tool,
            arguments=arguments or {},
            reason=reason,
            status="pending",
            requested_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(minutes=ttl_minutes)
        )
        db.add(approval)
        db.commit()
        db.refresh(approval)
        return approval

    @staticmethod
    def get_approval(db: Session, approval_id: str) -> Optional[ApprovalRequest]:
        return db.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id).first()

    @staticmethod
    def list_approvals(
        db: Session,
        status_filter: Optional[str] = None,
        agent_id: Optional[str] = None
    ) -> List[ApprovalRequest]:
        query = db.query(ApprovalRequest)
        if status_filter:
            query = query.filter(ApprovalRequest.status == status_filter)
        if agent_id:
            query = query.filter(ApprovalRequest.agent_id == agent_id)
        return query.order_by(ApprovalRequest.requested_at.desc()).all()

    @staticmethod
    def decide_approval(
        db: Session,
        approval_id: str,
        decision_in: ApprovalDecisionRequest
    ) -> ApprovalRequest:
        approval = db.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id).first()
        if not approval:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval request not found.")

        if approval.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Approval request already has status '{approval.status}' and cannot be modified."
            )

        if datetime.utcnow() > approval.expires_at:
            approval.status = "expired"
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Approval request has expired."
            )

        approval.status = decision_in.decision  # "approved" or "rejected"
        approval.decision = decision_in.decision
        approval.approver_id = decision_in.approver_id
        approval.decision_comment = decision_in.comment
        approval.decided_at = datetime.utcnow()

        db.commit()
        db.refresh(approval)

        # Audit the human decision
        AuditService.record_event(
            db=db,
            trace_id=approval.trace_id,
            agent_id=approval.agent_id,
            tool=approval.tool,
            decision=decision_in.decision,
            outcome=f"human_{decision_in.decision}",
            task_id=approval.task_id,
            arguments=approval.arguments,
            reason=f"Human supervisor '{decision_in.approver_id}' decided: {decision_in.decision}. {decision_in.comment or ''}"
        )

        return approval

    @staticmethod
    def validate_and_consume_approval(
        db: Session,
        approval_id: str,
        agent_id: str,
        tool: str
    ) -> bool:
        """
        Validates an approval for execution and marks it as 'consumed' (single-use guarantee).
        """
        approval = db.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id).first()
        if not approval:
            return False

        if approval.status != "approved":
            return False

        if approval.agent_id != agent_id or approval.tool != tool:
            return False

        if datetime.utcnow() > approval.expires_at:
            approval.status = "expired"
            db.commit()
            return False

        # Enforce single-use: Mark as consumed immediately
        approval.status = "consumed"
        db.commit()
        return True
