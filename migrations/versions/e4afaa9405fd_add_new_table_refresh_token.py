"""add new table refresh token

Revision ID: e4afaa9405fd
Revises: 3616f94fda8e
Create Date: 2025-06-10 22:22:21.713126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4afaa9405fd'
down_revision: Union[str, None] = '3616f94fda8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
