from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import User



class UserRepository:
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, user: User) -> User:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
