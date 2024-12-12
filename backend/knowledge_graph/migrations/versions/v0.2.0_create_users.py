"""create users table

Revision ID: v0.2.0
Revises: v0.1.0
Create Date: 2023-12-11 13:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'v0.2.0'
down_revision = 'v0.1.0'
branch_labels = None
depends_on = None

def upgrade():
    # 创建用户表
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', mysql.ENUM('ADMIN', 'USER', 'GUEST', name='user_role'),
                 nullable=False, server_default='USER'),
        sa.Column('status', mysql.ENUM('ACTIVE', 'INACTIVE', 'PENDING', 'DELETED', name='user_status'),
                 nullable=False, server_default='ACTIVE'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    
    # 添加索引
    op.create_index('idx_user_username', 'users', ['username'])
    op.create_index('idx_user_email', 'users', ['email'])

def downgrade():
    # 删除索引
    op.drop_index('idx_user_email', table_name='users')
    op.drop_index('idx_user_username', table_name='users')
    
    # 删除表
    op.drop_table('users')
    
    # 删除枚举类型
    op.execute('DROP TYPE IF EXISTS user_role')
    op.execute('DROP TYPE IF EXISTS user_status')