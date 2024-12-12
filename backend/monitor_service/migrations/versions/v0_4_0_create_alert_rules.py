"""create alert rules table

Revision ID: v0_4_0
Create Date: 2023-12-11 04:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'v0_4_0'
down_revision = 'v0_3_0'
branch_labels = None
depends_on = None

def upgrade():
    # 创建alert_rules表
    op.create_table(
        'alert_rules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.String(500)),
        sa.Column('metric_type', mysql.ENUM('cpu', 'memory', 'disk', 'network', 'system_load', 'process', name='metric_type'), nullable=False),
        sa.Column('operator', mysql.ENUM('>', '>=', '<', '<=', '==', '!=', name='comparison_operator'), nullable=False),
        sa.Column('threshold', sa.Float(), nullable=False),
        sa.Column('duration', sa.Integer(), default=0),
        sa.Column('enabled', sa.Boolean(), default=True),
        sa.Column('notify_methods', sa.JSON()),
        sa.Column('cooldown', sa.Integer(), default=300),
        sa.Column('last_triggered', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建索引
    op.create_index('ix_alert_rules_user_id', 'alert_rules', ['user_id'])
    op.create_index('ix_alert_rules_metric_type', 'alert_rules', ['metric_type'])

def downgrade():
    # 删除索引
    op.drop_index('ix_alert_rules_metric_type', 'alert_rules')
    op.drop_index('ix_alert_rules_user_id', 'alert_rules')
    
    # 删除表
    op.drop_table('alert_rules')
    
    # 删除枚举类型
    op.execute("DROP TYPE IF EXISTS metric_type")
    op.execute("DROP TYPE IF EXISTS comparison_operator") 