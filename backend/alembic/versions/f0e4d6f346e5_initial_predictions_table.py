"""initial_predictions_table

Revision ID: f0e4d6f346e5
Revises: 
Create Date: 2026-02-15 16:55:11.054943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0e4d6f346e5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "predictions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column("month", sa.Integer(), nullable=False),
        sa.Column("day_of_month", sa.Integer(), nullable=False),
        sa.Column("day_of_week", sa.Integer(), nullable=False),
        sa.Column("dep_time", sa.Integer(), nullable=False),
        sa.Column("carrier", sa.String(length=3), nullable=False),
        sa.Column("origin", sa.String(length=4), nullable=False),
        sa.Column("dest", sa.String(length=4), nullable=False),
        sa.Column("distance", sa.Integer(), nullable=False),
        sa.Column("model_name", sa.String(length=50), nullable=False),
        sa.Column("predicted_delayed", sa.Boolean(), nullable=False),
        sa.Column("delay_probability", sa.Float(), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("predictions")
