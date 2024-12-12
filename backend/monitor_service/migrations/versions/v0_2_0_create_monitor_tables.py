"""create monitor tables

Revision ID: v0_2_0
Create Date: 2023-12-11 02:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'v0_2_0'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 创建users表（如果不存在）
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('hashed_password', sa.String(200), nullable=False),
        sa.Column('email', sa.String(100)),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    
    # 创建monitor_settings表
    op.create_table(
        'monitor_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('login_alert', sa.Boolean(), default=True),
        sa.Column('operation_alert', sa.Boolean(), default=True),
        sa.Column('security_alert', sa.Boolean(), default=True),
        sa.Column('notify_methods', sa.JSON()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建monitor_alerts表
    op.create_table(
        'monitor_alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('alert_type', sa.String(50), nullable=False),
        sa.Column('level', sa.String(20), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('content', sa.Text()),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('handled_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建索引
    op.create_index('ix_monitor_settings_user_id', 'monitor_settings', ['user_id'])
    op.create_index('ix_monitor_alerts_user_id', 'monitor_alerts', ['user_id'])
    op.create_index('ix_monitor_alerts_alert_type', 'monitor_alerts', ['alert_type'])
    op.create_index('ix_monitor_alerts_level', 'monitor_alerts', ['level'])
    op.create_index('ix_monitor_alerts_status', 'monitor_alerts', ['status'])

def downgrade():
    # 删除索引
    op.drop_index('ix_monitor_alerts_status', 'monitor_alerts')
    op.drop_index('ix_monitor_alerts_level', 'monitor_alerts')
    op.drop_index('ix_monitor_alerts_alert_type', 'monitor_alerts')
    op.drop_index('ix_monitor_alerts_user_id', 'monitor_alerts')
    op.drop_index('ix_monitor_settings_user_id', 'monitor_settings')
    
    # 删除表
    op.drop_table('monitor_alerts')
    op.drop_table('monitor_settings')
    op.drop_table('users') 