"""Initial migration

Revision ID: 1a7a1bbeab89
Revises: 
Create Date: 2025-06-21 00:21:38.401894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '1a7a1bbeab89'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('hotels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('hotels')
