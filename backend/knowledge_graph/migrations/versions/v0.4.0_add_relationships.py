"""add relationships tables

Revision ID: v0.4.0
Revises: v0.3.1
Create Date: 2024-01-20 15:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'v0.4.0'
down_revision = 'v0.3.1'
branch_labels = None
depends_on = None

def upgrade():
    # 创建关系状态枚举
    op.execute("CREATE TYPE relationship_status AS ENUM ('active', 'inactive', 'pending', 'deleted')")
    
    # 创建关系类型枚举
    op.execute("""
        CREATE TYPE relationship_type AS ENUM (
            'prerequisite', 'related', 'includes', 'leads_to', 
            'mitigates', 'exploits', 'affects'
        )
    """)
    
    # 创建实体关系表
    op.create_table(
        'kg_entity_relationships',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('target_id', sa.Integer(), nullable=False),
        sa.Column('relationship_type', mysql.ENUM(
            'prerequisite', 'related', 'includes', 'leads_to',
            'mitigates', 'exploits', 'affects',
            name='relationship_type'
        ), nullable=False),
        sa.Column('properties', sa.JSON, nullable=True),
        sa.Column('status', mysql.ENUM(
            'active', 'inactive', 'pending', 'deleted',
            name='relationship_status'
        ), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['source_id'], ['kg_entities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_id'], ['kg_entities.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建前置知识关系表
    op.create_table(
        'kg_entity_prerequisites',
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('prerequisite_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['entity_id'], ['kg_entities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['prerequisite_id'], ['kg_entities.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('entity_id', 'prerequisite_id')
    )
    
    # 创建相关知识关系表
    op.create_table(
        'kg_entity_related',
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('related_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['entity_id'], ['kg_entities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['related_id'], ['kg_entities.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('entity_id', 'related_id')
    )
    
    # 添加索引
    op.create_index('idx_entity_relationships_source', 'kg_entity_relationships', ['source_id'])
    op.create_index('idx_entity_relationships_target', 'kg_entity_relationships', ['target_id'])
    op.create_index('idx_entity_relationships_type', 'kg_entity_relationships', ['relationship_type'])
    op.create_index('idx_entity_prerequisites', 'kg_entity_prerequisites', ['entity_id', 'prerequisite_id'])
    op.create_index('idx_entity_related', 'kg_entity_related', ['entity_id', 'related_id'])

def downgrade():
    # 删除索引
    op.drop_index('idx_entity_related', table_name='kg_entity_related')
    op.drop_index('idx_entity_prerequisites', table_name='kg_entity_prerequisites')
    op.drop_index('idx_entity_relationships_type', table_name='kg_entity_relationships')
    op.drop_index('idx_entity_relationships_target', table_name='kg_entity_relationships')
    op.drop_index('idx_entity_relationships_source', table_name='kg_entity_relationships')
    
    # 删除表
    op.drop_table('kg_entity_related')
    op.drop_table('kg_entity_prerequisites')
    op.drop_table('kg_entity_relationships')
    
    # 删除枚举类型
    op.execute('DROP TYPE IF EXISTS relationship_type')
    op.execute('DROP TYPE IF EXISTS relationship_status') 