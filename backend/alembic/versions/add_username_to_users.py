"""add username to users

Revision ID: add_username_to_users
Revises: 77b8659c2025
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_username_to_users'
down_revision = '77b8659c2025'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add username column to users table
    op.add_column('users', sa.Column('username', sa.String(255), nullable=False, server_default=''))
    
    # Create unique index for username
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)


def downgrade() -> None:
    # Drop the index first
    op.drop_index(op.f('ix_users_username'), table_name='users')
    
    # Drop the username column
    op.drop_column('users', 'username')
