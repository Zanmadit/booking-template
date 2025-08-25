"""baseline

Revision ID: a78cefed0775
Revises: 70809a958f3d
Create Date: 2025-04-08 22:26:12.619602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a78cefed0775'
down_revision: Union[str, None] = '70809a958f3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
