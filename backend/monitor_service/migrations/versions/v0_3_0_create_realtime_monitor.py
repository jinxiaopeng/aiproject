"""create realtime monitor tables

Revision ID: v0_3_0
Create Date: 2023-12-11 03:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'v0_3_0'
down_revision = 'v0_2_0'
branch_labels = None
depends_on = None

def upgrade():
    # 创建realtime_metrics表
    op.create_table(
        'realtime_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('metric_type', sa.String(50), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('metadata', sa.JSON()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建索引
    op.create_index('ix_realtime_metrics_user_id', 'realtime_metrics', ['user_id'])
    op.create_index('ix_realtime_metrics_metric_type', 'realtime_metrics', ['metric_type'])
    op.create_index('ix_realtime_metrics_timestamp', 'realtime_metrics', ['timestamp'])

def downgrade():
    # 删除索引
    op.drop_index('ix_realtime_metrics_timestamp', 'realtime_metrics')
    op.drop_index('ix_realtime_metrics_metric_type', 'realtime_metrics')
    op.drop_index('ix_realtime_metrics_user_id', 'realtime_metrics')
    
    # 删除表
    op.drop_table('realtime_metrics')