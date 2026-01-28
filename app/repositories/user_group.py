from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_group import UserGroup

class UserGroupRepository:
    async def get_by_name(self, db: AsyncSession, name: str) -> UserGroup:
        group = await db.scalar(select(UserGroup).where(UserGroup.name == name))
        if not group:
            raise ValueError("Group not found")
        return group
