"""Added rooms

Revision ID: ded7fcfe3b50
Revises: 1a7a1bbeab89
Create Date: 2025-06-21 01:14:54.969856

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ded7fcfe3b50"
down_revision: Union[str, Sequence[str], None] = "1a7a1bbeab89"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms")
