"""add default now() to timestamp

Revision ID: 6753be8804fb
Revises: 006decc26154
Create Date: 2025-05-30 20:05:15.107072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6753be8804fb'
down_revision: Union[str, None] = '006decc26154'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'image_records',
        'timestamp',
        server_default=sa.text('now()'),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=True,
    )


def downgrade():
    op.alter_column(
        'image_records',
        'timestamp',
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=True,
    )
