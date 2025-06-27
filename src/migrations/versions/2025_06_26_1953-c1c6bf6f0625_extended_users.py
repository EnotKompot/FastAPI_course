"""extended users

Revision ID: c1c6bf6f0625
Revises: e52e0b8d4e7a
Create Date: 2025-06-26 19:53:44.094942

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c1c6bf6f0625"
down_revision: Union[str, Sequence[str], None] = "e52e0b8d4e7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("first_name", sa.String(length=100), nullable=False)
    )
    op.add_column(
        "users", sa.Column("last_name", sa.String(length=100), nullable=False)
    )
    op.add_column("users", sa.Column("nickname", sa.String(length=100), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "nickname")
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
