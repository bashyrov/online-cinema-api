from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tokens import ActivationToken


class ActivationTokenRepository:
    async def create(self, db: AsyncSession, token: ActivationToken):
        db.add(token)
        await db.commit()
        await db.refresh(token)
        return token

    async def get(self, db: AsyncSession, token_str: ActivationToken):
        res = await db.execute(select(ActivationToken).where(ActivationToken.token == token_str))
        return res

    async def delete(self, db: AsyncSession, token_str: ActivationToken):
        await db.execute(delete(ActivationToken).where(ActivationToken.token == token_str))
        await db.commit()