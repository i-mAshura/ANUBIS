import json
import uuid
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc

from anubis.services.audit.models import AuditEvent
from anubis.services.audit.schemas import AuditVerificationResponse

GENESIS_PREV_HASH = "0" * 64
SENSITIVE_KEY_NAMES = {
    "api_key", "secret", "password", "token", "access_token",
    "private_key", "credential", "auth", "authorization", "bearer"
}


def redact_sensitive_arguments(args: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Recursively scrubs secrets, tokens, passwords, and private keys from audit payloads.
    """
    if not args:
        return {}

    scrubbed = {}
    for key, val in args.items():
        key_lower = str(key).lower()
        if any(sens in key_lower for sens in SENSITIVE_KEY_NAMES):
            scrubbed[key] = "[REDACTED_SECRET]"
        elif isinstance(val, dict):
            scrubbed[key] = redact_sensitive_arguments(val)
        elif isinstance(val, list):
            scrubbed[key] = [
                redact_sensitive_arguments(item) if isinstance(item, dict) else item
                for item in val
            ]
        elif isinstance(val, str) and (val.startswith("sec_") or val.startswith("eyJh")):
            # Redact suspected raw tokens / JWTs
            scrubbed[key] = "[REDACTED_TOKEN]"
        else:
            scrubbed[key] = val
    return scrubbed


def compute_audit_hash(
    prev_hash: str,
    seq: int,
    timestamp_iso: str,
    trace_id: str,
    task_id: str,
    agent_id: str,
    tool: str,
    decision: str,
    outcome: str,
    args_json: str
) -> str:
    """
    Deterministic SHA-256 hash calculation of canonical audit fields.
    """
    canonical_payload = (
        f"{prev_hash}|{seq}|{timestamp_iso}|{trace_id}|{task_id}|"
        f"{agent_id}|{tool}|{decision}|{outcome}|{args_json}"
    )
    return hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()


class AuditService:
    @staticmethod
    def record_event(
        db: Session,
        trace_id: str,
        agent_id: str,
        tool: str,
        decision: str,
        outcome: str,
        task_id: Optional[str] = "task-default",
        instance_id: Optional[str] = None,
        chain: Optional[List[str]] = None,
        arguments: Optional[Dict[str, Any]] = None,
        reason: Optional[str] = None,
        latency_ms: float = 0.0
    ) -> AuditEvent:
        """
        Appends an event to the tamper-evident hash-chained audit log.
        """
        # 1. Fetch latest audit event to establish the chain link
        last_event = db.query(AuditEvent).order_by(desc(AuditEvent.seq)).first()
        if last_event:
            seq = last_event.seq + 1
            prev_hash = last_event.hash
        else:
            seq = 1
            prev_hash = GENESIS_PREV_HASH

        # 2. Redact secrets from arguments
        args_redacted = redact_sensitive_arguments(arguments)
        args_json = json.dumps(args_redacted, sort_keys=True)

        # 3. Canonical timestamp
        now = datetime.utcnow()
        timestamp_iso = now.isoformat()

        # 4. Compute cryptographic hash
        event_hash = compute_audit_hash(
            prev_hash=prev_hash,
            seq=seq,
            timestamp_iso=timestamp_iso,
            trace_id=trace_id,
            task_id=task_id or "",
            agent_id=agent_id,
            tool=tool,
            decision=decision,
            outcome=outcome,
            args_json=args_json
        )

        event = AuditEvent(
            id=str(uuid.uuid4()),
            seq=seq,
            prev_hash=prev_hash,
            hash=event_hash,
            timestamp=now,
            trace_id=trace_id,
            task_id=task_id,
            agent_id=agent_id,
            instance_id=instance_id,
            chain=chain or [agent_id],
            tool=tool,
            args_redacted=args_redacted,
            decision=decision,
            reason=reason,
            outcome=outcome,
            latency_ms=round(latency_ms, 2)
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def verify_chain(db: Session) -> AuditVerificationResponse:
        """
        Mathematical verification of the entire audit chain.
        Detects any deleted records, inserted rows, or tampered values.
        """
        events = db.query(AuditEvent).order_by(AuditEvent.seq.asc()).all()
        if not events:
            return AuditVerificationResponse(
                verified=True,
                total_records=0,
                reason="Audit trail is empty (Genesis state)."
            )

        expected_prev_hash = GENESIS_PREV_HASH
        expected_seq = 1

        for event in events:
            # Check 1: Monotonic sequence continuity
            if event.seq != expected_seq:
                return AuditVerificationResponse(
                    verified=False,
                    total_records=len(events),
                    broken_at_seq=event.seq,
                    reason=f"Sequence gap detected: expected seq {expected_seq}, got {event.seq}."
                )

            # Check 2: Hash link continuity
            if event.prev_hash != expected_prev_hash:
                return AuditVerificationResponse(
                    verified=False,
                    total_records=len(events),
                    broken_at_seq=event.seq,
                    reason=f"Hash chain broken at seq {event.seq}: prev_hash does not match preceding record hash."
                )

            # Check 3: Recompute SHA-256 from payload
            args_json = json.dumps(event.args_redacted or {}, sort_keys=True)
            recalculated_hash = compute_audit_hash(
                prev_hash=event.prev_hash,
                seq=event.seq,
                timestamp_iso=event.timestamp.isoformat(),
                trace_id=event.trace_id,
                task_id=event.task_id or "",
                agent_id=event.agent_id,
                tool=event.tool,
                decision=event.decision,
                outcome=event.outcome,
                args_json=args_json
            )

            if event.hash != recalculated_hash:
                return AuditVerificationResponse(
                    verified=False,
                    total_records=len(events),
                    broken_at_seq=event.seq,
                    reason=f"Record tampering detected at seq {event.seq}: stored hash does not match computed content hash."
                )

            # Advance expected chain state
            expected_prev_hash = event.hash
            expected_seq += 1

        return AuditVerificationResponse(
            verified=True,
            total_records=len(events),
            latest_seq=events[-1].seq,
            latest_hash=events[-1].hash,
            genesis_hash=events[0].hash,
            reason="All audit records successfully verified against cryptographic hash chain."
        )

    @staticmethod
    def list_events(
        db: Session,
        agent_id: Optional[str] = None,
        tool: Optional[str] = None,
        decision: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[AuditEvent]:
        query = db.query(AuditEvent)
        if agent_id:
            query = query.filter(AuditEvent.agent_id == agent_id)
        if tool:
            query = query.filter(AuditEvent.tool == tool)
        if decision:
            query = query.filter(AuditEvent.decision == decision)
        return query.order_by(AuditEvent.seq.asc()).offset(offset).limit(limit).all()
