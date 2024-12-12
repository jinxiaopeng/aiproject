"""Add password column to users table

Revision ID: v0.7.0
Revises: v0.6.0
Create Date: 2024-12-09 21:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'v0.7.0'
down_revision = 'v0.6.0'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 添加 password 列
    op.add_column('users', sa.Column('password', sa.Text(), nullable=False, server_default=''))
    
def downgrade() -> None:
    # 删除 password 列
    op.drop_column('users', 'password') 