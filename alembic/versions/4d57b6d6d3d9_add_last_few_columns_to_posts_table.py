"""add last few columns to posts table

Revision ID: 4d57b6d6d3d9
Revises: 46c7c4c00952
Create Date: 2024-02-04 18:34:25.935543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d57b6d6d3d9'
down_revision: Union[str, None] = '46c7c4c00952'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column(
            'published',
            sa.Boolean(),
            nullable=False,
            server_default='TRUE'
        )
    )
    op.add_column(
        'posts',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(
                timezone=True
            ),
            nullable=False,
            server_default=sa.text('NOW()')
        )
    )

    pass


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    
    pass
