"""add foreign key to post table

Revision ID: 86230f7311de
Revises: d503dd818fbf
Create Date: 2026-03-07 07:45:07.374753

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "86230f7311de"
down_revision: Union[str, Sequence[str], None] = "d503dd818fbf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", column_name="owner_id")
    pass
