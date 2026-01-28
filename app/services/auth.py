from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password
from models import User
from repositories.user import UserRepository
from repositories.user_group import UserGroupRepository
from schemas.user import UserCreate


class AuthService:
    def __init__(self) -> None:
        self.users = UserRepository()
        self.groups = UserGroupRepository()

    async def register(self, db: AsyncSession, data: UserCreate) -> User:
        existing = await self.users.get_by_email(db, data.email)
        if existing:
            raise ValueError("Email already registered")

        group = await self.groups.get_by_name(db, "USER")

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            group_id=group.id,
            is_active=False,
        )
        return await self.users.create(db, user)