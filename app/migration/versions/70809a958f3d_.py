"""empty message

Revision ID: 70809a958f3d
Revises: cf596c8b397b
Create Date: 2025-04-08 22:19:13.772386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70809a958f3d'
down_revision: Union[str, None] = 'cf596c8b397b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
