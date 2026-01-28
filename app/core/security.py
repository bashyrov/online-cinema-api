from typing import Any

from passlib.context import CryptContext
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
)

class TokenError(Exception):
    pass


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(sub: str) -> str:
    exp = _utcnow() + timedelta(minutes=settings.ACCESS_TTL_MIN)
    payload: dict[str, Any] = {"sub": sub, "type": "access", "exp": exp, "iat": _utcnow()}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(sub: str) -> str:
    exp = _utcnow() + timedelta(days=settings.REFRESH_TTL_DAYS)
    payload: dict[str, Any] = {"sub": sub, "type": "refresh", "exp": exp, "iat": _utcnow()}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str, expected_type: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as e:
        raise TokenError("Invalid token") from e

    if payload.get("type") != expected_type:
        raise TokenError("Wrong token type")

    if not payload.get("sub"):
        raise TokenError("Missing subject")

    return payload