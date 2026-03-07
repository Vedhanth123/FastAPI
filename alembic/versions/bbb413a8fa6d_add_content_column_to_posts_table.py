"""Add content column to posts table

Revision ID: bbb413a8fa6d
Revises: c8de01901bac
Create Date: 2026-03-07 07:23:58.020282

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bbb413a8fa6d"
down_revision: Union[str, Sequence[str], None] = "c8de01901bac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
