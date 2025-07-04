"""Add: FacilitiesORM, RoomFacilitiesORM

Revision ID: 7c2df8829ae8
Revises: cb5a682c04da
Create Date: 2025-07-04 22:57:50.645977

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7c2df8829ae8"
down_revision: Union[str, Sequence[str], None] = "cb5a682c04da"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "facilities", ["id"])


def downgrade() -> None:
    op.drop_constraint(None, "facilities", type_="unique")
