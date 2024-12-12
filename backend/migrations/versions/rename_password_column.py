"""rename password column

Revision ID: rename_password_column
Revises: initial
Create Date: 2024-01-20

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'rename_password_column'
down_revision = 'initial'
branch_labels = None
depends_on = None

def upgrade():
    # 重命名 password 列为 hashed_password
    op.alter_column('users', 'password',
               new_column_name='hashed_password',
               existing_type=sa.Text(),
               existing_nullable=False)

def downgrade():
    # 还原：将 hashed_password 列改回 password
    op.alter_column('users', 'hashed_password',
               new_column_name='password',
               existing_type=sa.Text(),
               existing_nullable=False) 