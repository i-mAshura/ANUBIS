from typing import Optional
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from anubis.db import get_db
from anubis.services.auth.schemas import (
    ChallengeRequest, ChallengeResponse, TokenRequest, TokenResponse,
    KeypairGenerateResponse, TokenExchangeRequest
)
from anubis.services.auth.service import AuthService
from anubis.services.auth.crypto import generate_es256_keypair

router = APIRouter(tags=["Authentication & Tokens"])


def extract_bearer_token(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header. Expected 'Bearer <token>'."
        )
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected 'Bearer <token>'."
        )
    return parts[1]


@router.post("/auth/challenge", response_model=ChallengeResponse, status_code=status.HTTP_201_CREATED)
def request_challenge(request: ChallengeRequest, db: Session = Depends(get_db)):
    """
    Step 1 of Agent Authentication: Request a cryptographically secure nonce challenge.
    The agent must sign this challenge with its private key.
    """
    return AuthService.create_challenge(db, request)


@router.post("/auth/token", response_model=TokenResponse)
def issue_token(request: TokenRequest, db: Session = Depends(get_db)):
    """
    Step 2 of Agent Authentication: Submit signed challenge to receive a short-lived instance-bound JWT.
    """
    return AuthService.authenticate_and_issue_token(db, request)


@router.post("/auth/exchange", response_model=TokenResponse)
def exchange_token(
    request: TokenExchangeRequest,
    token: str = Depends(extract_bearer_token),
    db: Session = Depends(get_db)
):
    """
    Delegation Token Exchange:
    Parent agent exchanges its token for a narrowed token scoped to a sub-agent.
    Enforces the monotonic scope-subset rule and cryptographic 'act' lineage chain.
    """
    return AuthService.exchange_token(db, parent_token_str=token, request=request)


@router.post("/auth/keypair", response_model=KeypairGenerateResponse)
def generate_agent_keypair():
    """
    Utility endpoint to generate a new ECDSA P-256 (ES256) keypair for an AI agent runtime.
    """
    priv, pub = generate_es256_keypair()
    return KeypairGenerateResponse(
        private_key_pem=priv,
        public_key_pem=pub
    )
