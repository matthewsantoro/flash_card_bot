"""seed_initial_data

Revision ID: 693d2b0772bf
Revises: 281f42b6ba99
Create Date: 2025-01-21 10:23:31.527303

"""

from datetime import datetime, timezone 
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "693d2b0772bf"
down_revision: Union[str, None] = "281f42b6ba99"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    levels_table = sa.table(
        "levels",
        sa.column("level_id", sa.Integer),
        sa.column("interval_days", sa.Integer),
        sa.column("created", sa.DateTime),
        sa.column("updated", sa.DateTime),
    )

    op.bulk_insert(
        levels_table,
        [
            {
                "level_id": 1,
                "interval_days": 1,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "level_id": 2,
                "interval_days": 2,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "level_id": 3,
                "interval_days": 5,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "level_id": 4,
                "interval_days": 7,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "level_id": 5,
                "interval_days": 14,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "level_id": 6,
                "interval_days": 30,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
        ],
    )

    transitions_table = sa.table(
        "transitions",
        sa.column("transition_id", sa.Integer),
        sa.column("current_level_id", sa.Integer),
        sa.column("action_successful", sa.Boolean),
        sa.column("next_level_id", sa.Integer),
        sa.column("created", sa.DateTime),
        sa.column("updated", sa.DateTime),
    )
    op.bulk_insert(
        transitions_table,
        [
            {
                "current_level_id": 1,
                "action_successful": True,
                "next_level_id": 2,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "current_level_id": 1,
                "action_successful": False,
                "next_level_id": 1,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "current_level_id": 2,
                "action_successful": True,
                "next_level_id": 3,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "current_level_id": 2,
                "action_successful": False,
                "next_level_id": 1,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "current_level_id": 3,
                "action_successful": True,
                "next_level_id": 4,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "current_level_id": 3,
                "action_successful": False,
                "next_level_id": 2,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "current_level_id": 4,
                "action_successful": True,
                "next_level_id": 5,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "current_level_id": 4,
                "action_successful": False,
                "next_level_id": 3,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "current_level_id": 5,
                "action_successful": True,
                "next_level_id": 6,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "current_level_id": 5,
                "action_successful": False,
                "next_level_id": 2,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "current_level_id": 6,
                "action_successful": True,
                "next_level_id": 6,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
            {
                "current_level_id": 6,
                "action_successful": False,
                "next_level_id": 4,
                "created": datetime.now(timezone.utc).replace(tzinfo=None),
                "updated": datetime.now(timezone.utc).replace(tzinfo=None),
            },
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM transitions")
    op.execute("DELETE FROM levels")
