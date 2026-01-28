import enum

from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base


class UserGroupEnum(str, enum.Enum):
    USER = "USER"
    MODERATOR = "MODERATOR"
    ADMIN = "ADMIN"


class UserGroup(Base):
    __tablename__ = "user_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)