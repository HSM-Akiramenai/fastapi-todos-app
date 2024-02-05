"""add content column to posts table

Revision ID: fcf2f2bc229e
Revises: 6952717ea4d3
Create Date: 2024-02-04 03:33:29.914530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcf2f2bc229e'
down_revision: Union[str, None] = '6952717ea4d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
        )
    pass


def downgrade() -> None:
    op.drop_column(
        'posts',
        'content'
    )
    pass
