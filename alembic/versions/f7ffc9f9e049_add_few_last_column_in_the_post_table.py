"""add few last column in the post table

Revision ID: f7ffc9f9e049
Revises: 0b8354f9aef4
Create Date: 2025-01-25 09:54:53.593301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7ffc9f9e049'
down_revision: Union[str, None] = '0b8354f9aef4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column(
        "published",sa.Boolean(),nullable=False,
                                    server_default='True'))
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("NOW()")),)
    pass


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
