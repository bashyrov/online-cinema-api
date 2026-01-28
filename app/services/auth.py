from datetime import datetime, timezone, timedelta

from fastapi import Cookie, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.security import hash_password, verify_password, create_access_token, decode_token, TokenError, \
    create_refresh_token
from models import User, RefreshToken
from repositories.refresh_token import RefreshTokenRepository
from repositories.user import UserRepository
from repositories.user_group import UserGroupRepository
from schemas.user import UserCreate

def utcnow():
    return datetime.now(timezone.utc)


async def get_access_token_from_cookie(
    access_token: str | None = Cookie(default=None),
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return access_token


class AuthService:
    def __init__(self) -> None:
        self.users = UserRepository()
        self.groups = UserGroupRepository()
        self.refresh_repo = RefreshTokenRepository()
        #TODO later: self.activation_repo = ActivationTokenRepository()

    async def register(self, db: AsyncSession, user_data: UserCreate) -> User:
        existing = await self.users.get_by_email(db, user_data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        group = await self.groups.get_by_name(db, "USER")

        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            group_id=group.id,
            is_active=False,
        )
        user = await self.users.create(db, user)

        # TODO: create ActivationToken + send email
        # token_str = secrets.token_urlsafe(32)
        # expires_at = utcnow() + timedelta(hours=24)
        # activation = ActivationToken(user_id=user.id, token=token_str, expires_at=expires_at)
        # await self.activation_repo.create(db, activation)

        return user

    async def login(self, db: AsyncSession, email: str, password: str) -> dict:
        user = await self.users.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="Account is not activated")

        access = create_access_token(sub=str(user.id))
        refresh = create_refresh_token(sub=str(user.id))

        refresh_expires_at = utcnow() + timedelta(days=settings.REFRESH_TTL_DAYS)
        await self.refresh_repo.create(
            db,
            RefreshToken(
                user_id=user.id,
                token=refresh,
                expires_at=refresh_expires_at
            ),
        )

        return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

    async def refresh(self, db: AsyncSession, refresh_token: str) -> dict:
        try:
            payload = decode_token(refresh_token, expected_type="refresh")
        except TokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        row = await self.refresh_repo.get(db, refresh_token)
        if not row:
            raise HTTPException(status_code=401, detail="Refresh token revoked")

        user_id = payload["sub"]
        access = create_access_token(sub=str(user_id))
        return {"access_token": access, "token_type": "bearer"}

    async def logout(self, db: AsyncSession, refresh_token: str) -> None:
        await self.refresh_repo.delete(db, refresh_token)