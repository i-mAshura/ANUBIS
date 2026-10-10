import os
import uuid
import base64
import time
from typing import Tuple, Dict, Any, Optional
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import jwt


def generate_es256_keypair() -> Tuple[str, str]:
    """
    Generates an ECDSA P-256 keypair.
    Returns (private_key_pem, public_key_pem) as strings.
    """
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode("utf-8")

    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("utf-8")

    return private_pem, public_pem


def sign_challenge(private_key_pem: str, challenge_str: str) -> str:
    """
    Signs a challenge string using the private key (ECDSA with SHA-256).
    Returns URL-safe Base64 encoded signature.
    """
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"),
        password=None,
        backend=default_backend()
    )
    signature = private_key.sign(
        challenge_str.encode("utf-8"),
        ec.ECDSA(hashes.SHA256())
    )
    return base64.urlsafe_b64encode(signature).decode("utf-8")


def verify_challenge_signature(public_key_pem: str, challenge_str: str, signature_b64: str) -> bool:
    """
    Verifies ECDSA signature of a challenge string against the agent's public key.
    """
    try:
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode("utf-8"),
            backend=default_backend()
        )
        signature = base64.urlsafe_b64decode(signature_b64.encode("utf-8"))
        public_key.verify(
            signature,
            challenge_str.encode("utf-8"),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except Exception:
        return False


def public_key_to_jwk(public_key_pem: str, kid: str, alg: str = "ES256") -> Dict[str, Any]:
    """
    Converts an EC P-256 PEM public key into RFC 7517 JWK format.
    """
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode("utf-8"),
        backend=default_backend()
    )
    if not isinstance(public_key, ec.EllipticCurvePublicKey):
        raise ValueError("Key is not an EllipticCurvePublicKey")

    numbers = public_key.public_numbers()
    
    # Coordinates must be zero-padded to 32 bytes for P-256
    x_bytes = numbers.x.to_bytes(32, byteorder="big")
    y_bytes = numbers.y.to_bytes(32, byteorder="big")

    def b64url(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

    return {
        "kty": "EC",
        "crv": "P-256",
        "x": b64url(x_bytes),
        "y": b64url(y_bytes),
        "use": "sig",
        "alg": alg,
        "kid": kid
    }


class TokenService:
    """
    Signs and validates short-lived instance-bound JWTs for ANUBIS.
    """

    def __init__(self, private_key_pem: Optional[str] = None, kid: str = "anubis-key-1"):
        if private_key_pem:
            self.private_key_pem = private_key_pem
            self.private_key = serialization.load_pem_private_key(
                private_key_pem.encode("utf-8"), password=None, backend=default_backend()
            )
            self.public_key_pem = self.private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode("utf-8")
        else:
            self.private_key_pem, self.public_key_pem = generate_es256_keypair()
            self.private_key = serialization.load_pem_private_key(
                self.private_key_pem.encode("utf-8"), password=None, backend=default_backend()
            )
        self.kid = kid
        self.algorithm = "ES256"

    def get_jwks(self) -> Dict[str, Any]:
        jwk = public_key_to_jwk(self.public_key_pem, self.kid, self.algorithm)
        return {"keys": [jwk]}

    def issue_token(
        self,
        agent_id: str,
        instance_id: str,
        scope: list,
        task_id: Optional[str] = None,
        on_behalf_of: Optional[str] = None,
        delegation_chain: Optional[list] = None,
        parent_jti: Optional[str] = None,
        ttl_minutes: int = 15
    ) -> Dict[str, Any]:
        now = int(time.time())
        exp = now + (ttl_minutes * 60)
        jti = str(uuid.uuid4())

        payload = {
            "iss": "anubis-control-plane",
            "sub": agent_id,
            "instance_id": instance_id,
            "act": delegation_chain or [agent_id],
            "on_behalf_of": on_behalf_of or "system",
            "scope": scope,
            "task_id": task_id or "task-default",
            "parent_jti": parent_jti,
            "jti": jti,
            "iat": now,
            "nbf": now,
            "exp": exp
        }

        token = jwt.encode(
            payload,
            self.private_key_pem,
            algorithm=self.algorithm,
            headers={"kid": self.kid}
        )

        return {
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": ttl_minutes * 60,
            "jti": jti,
            "claims": payload
        }

    def verify_token(self, token_str: str) -> Dict[str, Any]:
        """
        Verifies token signature, expiration, and format.
        Raises jwt.PyJWTError on failure.
        """
        return jwt.decode(
            token_str,
            self.public_key_pem,
            algorithms=[self.algorithm],
            issuer="anubis-control-plane",
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iss": True,
                "require": ["sub", "instance_id", "jti", "exp", "scope"]
            }
        )
