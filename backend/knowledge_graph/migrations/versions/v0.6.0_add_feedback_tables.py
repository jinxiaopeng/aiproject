"""add feedback tables

Revision ID: v0.6.0
Revises: v0.5.0
Create Date: 2024-01-20 17:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'v0.6.0'
down_revision = 'v0.5.0'
branch_labels = None
depends_on = None

def upgrade():
    # 创建反馈表
    op.create_table(
        'kg_feedback',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('feedback_type', mysql.ENUM(
            'content', 'difficulty', 'suggestion', 'bug', 'other',
            name='feedback_type'
        ), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('status', mysql.ENUM(
            'pending', 'processing', 'resolved', 'rejected',
            name='feedback_status'
        ), nullable=False, server_default='pending'),
        sa.Column('admin_reply', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['entity_id'], ['kg_entities.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建反馈评论表
    op.create_table(
        'kg_feedback_comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('feedback_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['feedback_id'], ['kg_feedback.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建反馈投票表
    op.create_table(
        'kg_feedback_votes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('feedback_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('is_upvote', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['feedback_id'], ['kg_feedback.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 添加索引
    op.create_index('idx_feedback_user', 'kg_feedback', ['user_id'])
    op.create_index('idx_feedback_entity', 'kg_feedback', ['entity_id'])
    op.create_index('idx_feedback_type', 'kg_feedback', ['feedback_type'])
    op.create_index('idx_feedback_status', 'kg_feedback', ['status'])
    op.create_index('idx_feedback_comments_feedback', 'kg_feedback_comments', ['feedback_id'])
    op.create_index('idx_feedback_comments_user', 'kg_feedback_comments', ['user_id'])
    op.create_index('idx_feedback_votes_feedback', 'kg_feedback_votes', ['feedback_id'])
    op.create_index('idx_feedback_votes_user', 'kg_feedback_votes', ['user_id'])
    
    # 添加唯一约束，确保每个用户对每个反馈只能投票一次
    op.create_unique_constraint(
        'uq_feedback_votes_user_feedback',
        'kg_feedback_votes',
        ['user_id', 'feedback_id']
    )

def downgrade():
    # 删除唯一约束
    op.drop_constraint('uq_feedback_votes_user_feedback', 'kg_feedback_votes', type_='unique')
    
    # 删除索引
    op.drop_index('idx_feedback_votes_user', table_name='kg_feedback_votes')
    op.drop_index('idx_feedback_votes_feedback', table_name='kg_feedback_votes')
    op.drop_index('idx_feedback_comments_user', table_name='kg_feedback_comments')
    op.drop_index('idx_feedback_comments_feedback', table_name='kg_feedback_comments')
    op.drop_index('idx_feedback_status', table_name='kg_feedback')
    op.drop_index('idx_feedback_type', table_name='kg_feedback')
    op.drop_index('idx_feedback_entity', table_name='kg_feedback')
    op.drop_index('idx_feedback_user', table_name='kg_feedback')
    
    # 删除表
    op.drop_table('kg_feedback_votes')
    op.drop_table('kg_feedback_comments')
    op.drop_table('kg_feedback') 