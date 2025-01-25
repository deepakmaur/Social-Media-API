"""create posts table

Revision ID: 986d0b0b0c9b
Revises: 
Create Date: 2025-01-25 09:05:10.322507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '986d0b0b0c9b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('title',sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
