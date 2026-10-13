from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from anubis.db import get_db
from anubis.services.detection.schemas import AlertResponse, AlertUpdate, BaselineResponse
from anubis.services.detection.engine import DetectionEngine

router = APIRouter(prefix="", tags=["Detection"])


@router.get("/alerts", response_model=List[AlertResponse])
def list_alerts(
    agent_id: Optional[str] = Query(None, description="Filter alerts by agent ID"),
    severity: Optional[str] = Query(None, description="Filter alerts by severity"),
    rule: Optional[str] = Query(None, description="Filter alerts by rule name"),
    status: Optional[str] = Query(None, description="Filter alerts by status (active, acknowledged, resolved)"),
    db: Session = Depends(get_db)
):
    """Lists detection alerts matching the provided filters."""
    alerts = DetectionEngine.list_alerts(
        db=db,
        agent_id=agent_id,
        severity=severity,
        rule=rule,
        status_filter=status
    )
    return alerts


@router.patch("/alerts/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: str,
    update_in: AlertUpdate,
    db: Session = Depends(get_db)
):
    """Updates an alert status (e.g. acknowledge or resolve)."""
    return DetectionEngine.update_alert(db=db, alert_id=alert_id, update_in=update_in)


@router.get("/baselines/{agent_id}", response_model=BaselineResponse)
def get_agent_baseline(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Retrieves the learned behavioral baseline for an agent."""
    baseline = DetectionEngine.get_baseline(db=db, agent_id=agent_id)
    if not baseline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No behavioral baseline found for agent '{agent_id}'."
        )
    return baseline
