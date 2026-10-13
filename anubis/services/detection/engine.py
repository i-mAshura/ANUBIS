import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from sqlalchemy.orm import Session

from anubis.services.detection.models import Alert, AgentBaseline
from anubis.services.detection.schemas import AlertUpdate
from anubis.services.registry.models import Agent
from anubis.services.revocation.service import RevocationService
from anubis.services.revocation.schemas import RevocationCreate

# Sliding window buffers in memory: agent_id -> list of unix timestamps
_denial_windows: Dict[str, List[float]] = {}
_call_windows: Dict[str, List[float]] = {}

DENIAL_BURST_THRESHOLD = 5     # 5 denials in 60s triggers immediate kill switch suspension
DENIAL_WINDOW_SECONDS = 60
VOLUME_SPIKE_THRESHOLD = 30    # 30 calls in 60s triggers volume alert


class DetectionEngine:
    @classmethod
    def clear_buffers(cls):
        """Clears sliding window buffers (useful for test resets)."""
        _denial_windows.clear()
        _call_windows.clear()

    @classmethod
    def inspect_and_record(
        cls,
        db: Session,
        agent_id: str,
        tool_name: str,
        decision: str,
        arguments: Optional[Dict[str, Any]] = None
    ) -> List[Alert]:
        """
        Analyzes call telemetry, evaluates anomaly detection rules, updates baselines,
        and triggers automated retribution actions (alerts, suspension, kill switch).
        """
        now = time.time()
        now_dt = datetime.utcnow()
        triggered_alerts: List[Alert] = []

        # 1. Update sliding window call rate
        calls = _call_windows.setdefault(agent_id, [])
        calls.append(now)
        _call_windows[agent_id] = [t for t in calls if now - t <= 60]

        # 2. Volume Spike Detection
        if len(_call_windows[agent_id]) > VOLUME_SPIKE_THRESHOLD:
            vol_alert = Alert(
                id=f"alt_{uuid.uuid4().hex[:12]}",
                agent_id=agent_id,
                rule="volume_spike",
                severity="medium",
                details={
                    "calls_in_window": len(_call_windows[agent_id]),
                    "window_seconds": 60,
                    "tool": tool_name
                },
                action_taken="alert",
                status="active",
                created_at=now_dt
            )
            db.add(vol_alert)
            triggered_alerts.append(vol_alert)

        # 3. Retrieve or initialize behavioral baseline
        baseline = db.query(AgentBaseline).filter(AgentBaseline.agent_id == agent_id).first()
        if not baseline:
            baseline = AgentBaseline(
                id=f"base_{uuid.uuid4().hex[:12]}",
                agent_id=agent_id,
                known_tools=[],
                total_calls=0,
                total_denials=0,
                last_seen_at=now_dt
            )
            db.add(baseline)
            db.commit()
            db.refresh(baseline)

        known_tools_list = list(baseline.known_tools or [])

        # 4. Novel Tool Probing Rule
        # If agent has a baseline history and calls a tool it has never invoked before
        if baseline.total_calls >= 2 and tool_name not in known_tools_list:
            novel_alert = Alert(
                id=f"alt_{uuid.uuid4().hex[:12]}",
                agent_id=agent_id,
                rule="novel_tool_probe",
                severity="low",
                details={
                    "tool": tool_name,
                    "known_tools_count": len(known_tools_list),
                    "known_tools": known_tools_list
                },
                action_taken="alert",
                status="active",
                created_at=now_dt
            )
            db.add(novel_alert)
            triggered_alerts.append(novel_alert)

        # 5. Off-Hours Activity Detection (between 00:00 and 05:00 UTC)
        if 0 <= now_dt.hour < 5:
            off_hours_alert = Alert(
                id=f"alt_{uuid.uuid4().hex[:12]}",
                agent_id=agent_id,
                rule="off_hours_activity",
                severity="low",
                details={"hour_utc": now_dt.hour, "tool": tool_name},
                action_taken="alert",
                status="active",
                created_at=now_dt
            )
            db.add(off_hours_alert)
            triggered_alerts.append(off_hours_alert)

        # 6. Denial Burst Rule & Automated Retribution
        if decision == "deny":
            denials = _denial_windows.setdefault(agent_id, [])
            denials.append(now)
            _denial_windows[agent_id] = [t for t in denials if now - t <= DENIAL_WINDOW_SECONDS]
            recent_denials_count = len(_denial_windows[agent_id])

            baseline.total_denials += 1

            if recent_denials_count >= DENIAL_BURST_THRESHOLD:
                # AUTOMATED RETRIBUTION: Suspend agent and trigger kill switch!
                burst_alert = Alert(
                    id=f"alt_{uuid.uuid4().hex[:12]}",
                    agent_id=agent_id,
                    rule="denial_burst",
                    severity="critical",
                    details={
                        "denied_count": recent_denials_count,
                        "window_seconds": DENIAL_WINDOW_SECONDS,
                        "last_denied_tool": tool_name
                    },
                    action_taken="suspend",
                    status="active",
                    created_at=now_dt
                )
                db.add(burst_alert)
                triggered_alerts.append(burst_alert)

                # Suspend agent in database
                agent = db.query(Agent).filter(Agent.id == agent_id).first()
                if agent:
                    agent.status = "suspended"

                # Trigger kill switch immediate revocation
                RevocationService.revoke(
                    db=db,
                    rev_in=RevocationCreate(
                        target_type="agent",
                        target_id=agent_id,
                        reason=f"Automated Anomaly Response: Burst of {recent_denials_count} denied calls in {DENIAL_WINDOW_SECONDS}s.",
                        revoked_by="anubis-detection-engine"
                    )
                )

        # 7. Update baseline statistics
        baseline.total_calls += 1
        if tool_name not in known_tools_list:
            known_tools_list.append(tool_name)
            baseline.known_tools = known_tools_list
        baseline.last_seen_at = now_dt

        db.commit()
        return triggered_alerts

    @staticmethod
    def list_alerts(
        db: Session,
        agent_id: Optional[str] = None,
        severity: Optional[str] = None,
        rule: Optional[str] = None,
        status_filter: Optional[str] = None
    ) -> List[Alert]:
        query = db.query(Alert)
        if agent_id:
            query = query.filter(Alert.agent_id == agent_id)
        if severity:
            query = query.filter(Alert.severity == severity)
        if rule:
            query = query.filter(Alert.rule == rule)
        if status_filter:
            query = query.filter(Alert.status == status_filter)
        return query.order_by(Alert.created_at.desc()).all()

    @staticmethod
    def update_alert(db: Session, alert_id: str, update_in: AlertUpdate) -> Alert:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Alert not found.")
        alert.status = update_in.status
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def get_baseline(db: Session, agent_id: str) -> Optional[AgentBaseline]:
        return db.query(AgentBaseline).filter(AgentBaseline.agent_id == agent_id).first()
