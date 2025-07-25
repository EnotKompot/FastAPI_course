"""Upd users - extended password length

Revision ID: 577faffbaddd
Revises: c1c6bf6f0625
Create Date: 2025-06-26 20:24:09.384738

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "577faffbaddd"
down_revision: Union[str, Sequence[str], None] = "c1c6bf6f0625"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=200),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.String(length=200),
        type_=sa.VARCHAR(length=50),
        existing_nullable=False,
    )
