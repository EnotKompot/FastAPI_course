"""Upd RoomsORM - updated fields params

Revision ID: 162a7f0214c4
Revises: c3b45fd22042
Create Date: 2025-06-29 21:26:57.957806

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "162a7f0214c4"
down_revision: Union[str, Sequence[str], None] = "c3b45fd22042"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("rooms", "title", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("rooms", "description", existing_type=sa.VARCHAR(), nullable=True)


def downgrade() -> None:
    op.alter_column("rooms", "description", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("rooms", "title", existing_type=sa.VARCHAR(), nullable=True)
