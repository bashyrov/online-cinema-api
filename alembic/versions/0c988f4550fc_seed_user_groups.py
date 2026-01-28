"""seed user groups

Revision ID: 0c988f4550fc
Revises: 6b7a2c2669ed
Create Date: 2026-01-28 18:05:22.362694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c988f4550fc'
down_revision: Union[str, Sequence[str], None] = '6b7a2c2669ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_groups = sa.table(
        "user_groups",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
    )

    op.bulk_insert(
        user_groups,
        [
            {"name": "USER"},
            {"name": "MODERATOR"},
            {"name": "ADMIN"},
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM user_groups WHERE name IN ('USER','MODERATOR','ADMIN')")