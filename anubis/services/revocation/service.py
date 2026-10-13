import uuid
from datetime import datetime
from typing import List, Optional, Tuple, Set
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from anubis.services.revocation.models import RevocationEntry
from anubis.services.revocation.schemas import RevocationCreate

# Fast in-memory cache of active revocation keys: format "{target_type}:{target_id}"
_active_revocations: Set[str] = set()


class RevocationService:
    @staticmethod
    def _cache_key(target_type: str, target_id: str) -> str:
        return f"{target_type.lower()}:{target_id}"

    @classmethod
    def clear_cache(cls):
        _active_revocations.clear()

    @classmethod
    def initialize_cache_from_db(cls, db: Session):
        """Loads all active revocations into memory cache on startup."""
        _active_revocations.clear()
        entries = db.query(RevocationEntry).filter(RevocationEntry.active == True).all()
        for e in entries:
            _active_revocations.add(cls._cache_key(e.target_type, e.target_id))

    @classmethod
    def revoke(cls, db: Session, rev_in: RevocationCreate) -> RevocationEntry:
        """
        Executes immediate kill switch for an agent, instance, task, token, or human principal.
        Takes effect immediately in cache and persists to DB.
        """
        entry = RevocationEntry(
            id=f"rev_{uuid.uuid4().hex[:12]}",
            target_type=rev_in.target_type.lower(),
            target_id=rev_in.target_id,
            reason=rev_in.reason,
            revoked_by=rev_in.revoked_by or "admin",
            revoked_at=datetime.utcnow(),
            active=True
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)

        # Update real-time memory cache immediately
        _active_revocations.add(cls._cache_key(entry.target_type, entry.target_id))
        return entry

    @classmethod
    def is_revoked(cls, target_type: str, target_id: Optional[str]) -> bool:
        if not target_id:
            return False
        return cls._cache_key(target_type, target_id) in _active_revocations

    @classmethod
    def check_hierarchy_revoked(
        cls,
        agent_id: str,
        instance_id: Optional[str] = None,
        task_id: Optional[str] = None,
        jti: Optional[str] = None,
        principal: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Multi-dimensional kill switch validation:
        Blocks if the agent, instance, task, token, or principal is revoked.
        """
        if cls.is_revoked("agent", agent_id):
            return True, f"Agent '{agent_id}' has been terminated by kill switch."
        if instance_id and cls.is_revoked("instance", instance_id):
            return True, f"Instance '{instance_id}' has been terminated."
        if task_id and cls.is_revoked("task", task_id):
            return True, f"Task '{task_id}' has been revoked."
        if jti and cls.is_revoked("token", jti):
            return True, f"Token '{jti}' has been blacklisted."
        if principal and cls.is_revoked("principal", principal):
            return True, f"Human principal '{principal}' has been suspended."

        return False, None

    @classmethod
    def list_revocations(cls, db: Session, active_only: bool = True) -> List[RevocationEntry]:
        query = db.query(RevocationEntry)
        if active_only:
            query = query.filter(RevocationEntry.active == True)
        return query.order_by(RevocationEntry.revoked_at.desc()).all()

    @classmethod
    def deactivate_revocation(cls, db: Session, rev_id: str) -> RevocationEntry:
        entry = db.query(RevocationEntry).filter(RevocationEntry.id == rev_id).first()
        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Revocation entry not found.")
        entry.active = False
        db.commit()
        db.refresh(entry)
        _active_revocations.discard(cls._cache_key(entry.target_type, entry.target_id))
        return entry
