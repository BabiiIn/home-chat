"""increase password_hash length

Revision ID: a1f2836ad805
Revises: 21f8375e7f66
Create Date: 2026-07-11 14:44:58.969925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1f2836ad805'
down_revision: Union[str, Sequence[str], None] = '21f8375e7f66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
    'users',
    'password_hash',
    existing_type=sa.String(),
    type_=sa.String(255),
    nullable=False
)

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
    'users',
    'password_hash',
    existing_type=sa.String(255),
    type_=sa.String(),
    nullable=False
)

    pass
