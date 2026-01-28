from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tokens import RefreshToken


class RefreshTokenRepository:
    async def create(self, db: AsyncSession, token: RefreshToken) -> RefreshToken:
        db.add(token)
        await db.commit()
        await db.refresh(token)
        return token

    async def get(self, db: AsyncSession, token_str: str) -> RefreshToken | None:
        res = await db.execute(select(RefreshToken).where(RefreshToken.token == token_str))
        return res.scalar_one_or_none()

    async def delete(self, db: AsyncSession, token_str: str) -> None:
        await db.execute(delete(RefreshToken).where(RefreshToken.token == token_str))
        await db.commit()