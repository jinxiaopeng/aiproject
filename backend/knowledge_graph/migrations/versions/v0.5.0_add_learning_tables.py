"""add learning tables

Revision ID: v0.5.0
Revises: v0.4.0
Create Date: 2024-01-20 16:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'v0.5.0'
down_revision = 'v0.4.0'
branch_labels = None
depends_on = None

def upgrade():
    # 创建学习记录表
    op.create_table(
        'kg_learning_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('status', mysql.ENUM(
            'not_started', 'in_progress', 'completed', 'reviewing',
            name='learning_status'
        ), nullable=False, server_default='not_started'),
        sa.Column('progress', sa.Float(), nullable=False, server_default='0'),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('last_study_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['entity_id'], ['kg_entities.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建学习会话表
    op.create_table(
        'kg_study_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('learning_record_id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('progress_delta', sa.Float(), nullable=False, server_default='0'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['learning_record_id'], ['kg_learning_records.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建测试记录表
    op.create_table(
        'kg_test_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('learning_record_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('max_score', sa.Float(), nullable=False, server_default='100'),
        sa.Column('test_time', sa.DateTime(), nullable=False),
        sa.Column('answers', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['learning_record_id'], ['kg_learning_records.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 添加索引
    op.create_index('idx_learning_records_user', 'kg_learning_records', ['user_id'])
    op.create_index('idx_learning_records_entity', 'kg_learning_records', ['entity_id'])
    op.create_index('idx_learning_records_status', 'kg_learning_records', ['status'])
    op.create_index('idx_study_sessions_record', 'kg_study_sessions', ['learning_record_id'])
    op.create_index('idx_test_records_record', 'kg_test_records', ['learning_record_id'])

def downgrade():
    # 删除索引
    op.drop_index('idx_test_records_record', table_name='kg_test_records')
    op.drop_index('idx_study_sessions_record', table_name='kg_study_sessions')
    op.drop_index('idx_learning_records_status', table_name='kg_learning_records')
    op.drop_index('idx_learning_records_entity', table_name='kg_learning_records')
    op.drop_index('idx_learning_records_user', table_name='kg_learning_records')
    
    # 删除表
    op.drop_table('kg_test_records')
    op.drop_table('kg_study_sessions')
    op.drop_table('kg_learning_records')