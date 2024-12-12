"""create practice tables

Revision ID: create_practice_tables
Revises: create_course_tables
Create Date: 2024-01-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'create_practice_tables'
down_revision = 'create_course_tables'
branch_labels = None
depends_on = None

def upgrade():
    # 创建靶场表
    op.create_table(
        'practice_labs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('difficulty', sa.String(20), nullable=False),
        sa.Column('points', sa.Integer(), nullable=False, default=100),
        sa.Column('docker_image', sa.String(255), nullable=False),
        sa.Column('port_mapping', sa.String(50), nullable=False),
        sa.Column('flag', sa.String(255), nullable=True),
        sa.Column('hints', mysql.JSON(), nullable=True),
        sa.Column('resource_limits', mysql.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建靶场实例表
    op.create_table(
        'practice_instances',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lab_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('container_id', sa.String(100), nullable=True),
        sa.Column('instance_url', sa.String(255), nullable=True),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['lab_id'], ['practice_labs.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建靶场进度表
    op.create_table(
        'practice_progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lab_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False, default=0),
        sa.Column('attempts', sa.Integer(), nullable=False, default=0),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['lab_id'], ['practice_labs.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建索引
    op.create_index('ix_practice_labs_title', 'practice_labs', ['title'])
    op.create_index('ix_practice_labs_category', 'practice_labs', ['category'])
    op.create_index('ix_practice_labs_difficulty', 'practice_labs', ['difficulty'])
    op.create_index('ix_practice_instances_lab_id', 'practice_instances', ['lab_id'])
    op.create_index('ix_practice_instances_user_id', 'practice_instances', ['user_id'])
    op.create_index('ix_practice_instances_status', 'practice_instances', ['status'])
    op.create_index('ix_practice_progress_lab_id', 'practice_progress', ['lab_id'])
    op.create_index('ix_practice_progress_user_id', 'practice_progress', ['user_id'])
    op.create_index('ix_practice_progress_status', 'practice_progress', ['status'])

def downgrade():
    # 删除索引
    op.drop_index('ix_practice_progress_status', 'practice_progress')
    op.drop_index('ix_practice_progress_user_id', 'practice_progress')
    op.drop_index('ix_practice_progress_lab_id', 'practice_progress')
    op.drop_index('ix_practice_instances_status', 'practice_instances')
    op.drop_index('ix_practice_instances_user_id', 'practice_instances')
    op.drop_index('ix_practice_instances_lab_id', 'practice_instances')
    op.drop_index('ix_practice_labs_difficulty', 'practice_labs')
    op.drop_index('ix_practice_labs_category', 'practice_labs')
    op.drop_index('ix_practice_labs_title', 'practice_labs')

    # 删除表
    op.drop_table('practice_progress')
    op.drop_table('practice_instances')
    op.drop_table('practice_labs') 