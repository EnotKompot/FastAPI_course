"""Upd users

Revision ID: c3b45fd22042
Revises: 577faffbaddd
Create Date: 2025-06-26 20:26:19.988544

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c3b45fd22042"
down_revision: Union[str, Sequence[str], None] = "577faffbaddd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users", "first_name", existing_type=sa.VARCHAR(length=100), nullable=True
    )
    op.alter_column(
        "users", "last_name", existing_type=sa.VARCHAR(length=100), nullable=True
    )


def downgrade() -> None:
    op.alter_column(
        "users", "last_name", existing_type=sa.VARCHAR(length=100), nullable=False
    )
    op.alter_column(
        "users", "first_name", existing_type=sa.VARCHAR(length=100), nullable=False
    )
