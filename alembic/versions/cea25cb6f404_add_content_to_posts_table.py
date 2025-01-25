"""add content to posts table

Revision ID: cea25cb6f404
Revises: 986d0b0b0c9b
Create Date: 2025-01-25 09:18:46.106990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cea25cb6f404'
down_revision: Union[str, None] = '986d0b0b0c9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
