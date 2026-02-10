"""convert goal_flags to jsonb

Revision ID: 78bac3192825
Revises: a5ac723d2b68
Create Date: 2025-11-21 15:42:54.619633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '78bac3192825'
down_revision: Union[str, Sequence[str], None] = 'a5ac723d2b68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Convert goal_flags from JSON → JSONB
    op.alter_column(
        "meal_library",
        "goal_flags",
        type_=sa.JSON().with_variant(postgresql.JSONB(), "postgresql"),
        postgresql_using="goal_flags::jsonb"
    )

def downgrade():
    op.alter_column(
        "meal_library",
        "goal_flags",
        type_=sa.JSON(),
        postgresql_using="goal_flags::json"
    )

