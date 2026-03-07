"""add created_at

Revision ID: ef874f485cd5
Revises: 86230f7311de
Create Date: 2026-03-07 07:48:47.317180

"""

from typing import Sequence, Union

from alembic import op
from rich import text
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ef874f485cd5"
down_revision: Union[str, Sequence[str], None] = "86230f7311de"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column("posts", sa.Column("published", sa.Boolean(), server_default="TRUE"))
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")

    pass
