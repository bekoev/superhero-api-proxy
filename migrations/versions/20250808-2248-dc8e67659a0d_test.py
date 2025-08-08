"""test

Revision ID: dc8e67659a0d
Revises:
Create Date: 2025-08-08 22:48:16.319533

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dc8e67659a0d"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "heroes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "powerstats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("intelligence", sa.Integer(), nullable=True),
        sa.Column("strength", sa.Integer(), nullable=True),
        sa.Column("speed", sa.Integer(), nullable=True),
        sa.Column("power", sa.Integer(), nullable=True),
        sa.Column("hero_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hero_id"],
            ["heroes.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("powerstats")
    op.drop_table("heroes")
