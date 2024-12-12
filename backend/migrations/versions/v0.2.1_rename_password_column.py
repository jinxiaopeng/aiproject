"""rename password column

Revision ID: v0.2.1
Revises: v0.2.0
Create Date: 2024-01-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'v0.2.1'
down_revision: Union[str, None] = 'v0.2.0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 重命名 password 列为 hashed_password
    op.alter_column('users', 'password',
               new_column_name='hashed_password',
               existing_type=sa.String(length=255),
               existing_nullable=True)

def downgrade() -> None:
    # 还原：将 hashed_password 列改回 password
    op.alter_column('users', 'hashed_password',
               new_column_name='password',
               existing_type=sa.String(length=255),
               existing_nullable=True) 