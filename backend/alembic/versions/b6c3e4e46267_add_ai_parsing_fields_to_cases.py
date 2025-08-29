"""add_ai_parsing_fields_to_cases

Revision ID: b6c3e4e46267
Revises: add_username_to_users
Create Date: 2025-08-29 13:02:38.458042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6c3e4e46267'
down_revision: Union[str, Sequence[str], None] = 'add_username_to_users'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new columns for AI parsing fields
    op.add_column('cases', sa.Column('guest', sa.String(255), nullable=True))
    op.add_column('cases', sa.Column('created', sa.String(100), nullable=True))
    op.add_column('cases', sa.Column('created_by', sa.String(255), nullable=True))
    op.add_column('cases', sa.Column('modified', sa.String(100), nullable=True))
    op.add_column('cases', sa.Column('modified_by', sa.String(255), nullable=True))
    op.add_column('cases', sa.Column('source', sa.String(255), nullable=True))
    op.add_column('cases', sa.Column('membership', sa.String(255), nullable=True))
    op.add_column('cases', sa.Column('case_description', sa.Text(), nullable=True))
    op.add_column('cases', sa.Column('in_out', sa.String(255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the added columns
    op.drop_column('cases', 'guest')
    op.drop_column('cases', 'created')
    op.drop_column('cases', 'created_by')
    op.drop_column('cases', 'modified')
    op.drop_column('cases', 'modified_by')
    op.drop_column('cases', 'source')
    op.drop_column('cases', 'membership')
    op.drop_column('cases', 'case_description')
    op.drop_column('cases', 'in_out')
