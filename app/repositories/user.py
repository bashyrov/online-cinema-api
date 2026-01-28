from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.security import hash_password
from models import User
from repositories.user_group import UserGroupRepository
from schemas.user import UserCreate


async def create_user(db: AsyncSession, user: UserCreate):
    hashed = hash_password(user.password)

    group = await UserGroupRepository.get_by_name(db, "USER")
    db_user = User(email=user.email, hashed_password=hashed, group_id=group.id)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()
