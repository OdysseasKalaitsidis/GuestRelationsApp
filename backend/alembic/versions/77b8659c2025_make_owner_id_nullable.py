"""make_owner_id_nullable

Revision ID: 77b8659c2025
Revises: 25dc53a539a3
Create Date: 2025-08-24 13:38:00.230822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77b8659c2025'
down_revision: Union[str, Sequence[str], None] = '25dc53a539a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Make owner_id nullable in cases table
    op.alter_column('cases', 'owner_id',
                    existing_type=sa.Integer(),
                    nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Make owner_id not nullable in cases table
    op.alter_column('cases', 'owner_id',
                    existing_type=sa.Integer(),
                    nullable=False)
