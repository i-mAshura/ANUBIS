import uuid
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from anubis.config import settings
from anubis.services.registry.models import Agent
from anubis.services.auth.crypto import (
    TokenService, verify_challenge_signature, generate_es256_keypair
)
from anubis.services.auth.schemas import (
    ChallengeRequest, ChallengeResponse, TokenRequest, TokenResponse
)

# Global TokenService instance for server token signing
token_service = TokenService(
    private_key_pem=settings.SERVER_PRIVATE_KEY_PEM,
    kid=settings.SERVER_KID
)

# In-memory challenge store (can be backed by Redis in distributed setups)
# Maps challenge_id -> {"agent_id": str, "instance_id": str, "challenge": str, "expires_at": datetime, "consumed": bool}
_challenges: Dict[str, Dict[str, Any]] = {}


class AuthService:
    @staticmethod
    def get_jwks() -> Dict[str, Any]:
        return token_service.get_jwks()

    @staticmethod
    def create_challenge(db: Session, request: ChallengeRequest) -> ChallengeResponse:
        agent = db.query(Agent).filter(Agent.id == request.agent_id).first()
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent '{request.agent_id}' is not registered."
            )
        if agent.status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Agent '{request.agent_id}' is {agent.status}. Only active agents may authenticate."
            )
        if agent.expires_at and agent.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Agent registration has expired on {agent.expires_at}."
            )

        challenge_id = str(uuid.uuid4())
        nonce = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(seconds=settings.CHALLENGE_TTL_SECONDS)

        _challenges[challenge_id] = {
            "agent_id": request.agent_id,
            "instance_id": request.instance_id or "inst-primary",
            "challenge": nonce,
            "expires_at": expires_at,
            "consumed": False
        }

        return ChallengeResponse(
            challenge_id=challenge_id,
            agent_id=request.agent_id,
            challenge=nonce,
            expires_at=expires_at
        )

    @staticmethod
    def authenticate_and_issue_token(db: Session, request: TokenRequest) -> TokenResponse:
        # 1. Lookup challenge
        challenge_data = _challenges.get(request.challenge_id)
        if not challenge_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired challenge ID."
            )

        # 2. Replay & Expiry Check
        if challenge_data["consumed"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Challenge has already been consumed (replay attack detected)."
            )
        if datetime.utcnow() > challenge_data["expires_at"]:
            _challenges.pop(request.challenge_id, None)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Challenge has expired."
            )
        if challenge_data["agent_id"] != request.agent_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Challenge agent mismatch."
            )

        # Immediately mark consumed to prevent parallel replays
        challenge_data["consumed"] = True

        # 3. Verify Agent status
        agent = db.query(Agent).filter(Agent.id == request.agent_id).first()
        if not agent or agent.status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Agent is not registered or not active."
            )

        # 4. Verify cryptographic signature against registered public key
        is_valid = verify_challenge_signature(
            public_key_pem=agent.public_key,
            challenge_str=challenge_data["challenge"],
            signature_b64=request.signature
        )

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cryptographic signature verification failed. Possession of agent private key not proven."
            )

        # 5. Issue short-lived JWT token
        token_info = token_service.issue_token(
            agent_id=agent.id,
            instance_id=request.instance_id,
            scope=request.requested_scope or ["tools:read"],
            task_id=request.task_id,
            on_behalf_of=request.on_behalf_of,
            delegation_chain=[agent.id],
            ttl_minutes=settings.TOKEN_DEFAULT_TTL_MINUTES
        )

        return TokenResponse(
            access_token=token_info["access_token"],
            token_type=token_info["token_type"],
            expires_in=token_info["expires_in"],
            jti=token_info["jti"],
            claims=token_info["claims"]
        )
