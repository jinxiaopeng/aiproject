"""initial migration

Revision ID: v0.1.0
Revises: 
Create Date: 2023-12-11 12:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'v0.1.0'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 创建基础实体表
    op.create_table(
        'kg_entities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('properties', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('status', mysql.ENUM('active', 'inactive', 'pending', 'deleted', name='entity_status'),
                 nullable=False, server_default='active'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建攻击类型表
    op.create_table(
        'kg_attack_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('impact', sa.Text(), nullable=True),
        sa.Column('mitigation', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('status', mysql.ENUM('active', 'inactive', 'pending', 'deleted', name='attack_status'),
                 nullable=False, server_default='active'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建漏洞表
    op.create_table(
        'kg_vulnerabilities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cve_id', sa.String(20), nullable=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity', mysql.ENUM('high', 'medium', 'low', name='vulnerability_severity'),
                 nullable=False, server_default='medium'),
        sa.Column('affected_systems', sa.JSON, nullable=True),
        sa.Column('solution', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('status', mysql.ENUM('active', 'inactive', 'pending', 'deleted', name='vulnerability_status'),
                 nullable=False, server_default='active'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建实体关系表
    op.create_table(
        'kg_entity_relationships',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('target_id', sa.Integer(), nullable=False),
        sa.Column('relationship_type', sa.String(50), nullable=False),
        sa.Column('properties', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['source_id'], ['kg_entities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_id'], ['kg_entities.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 添加索引
    op.create_index('idx_entity_name', 'kg_entities', ['name'])
    op.create_index('idx_entity_type', 'kg_entities', ['entity_type'])
    op.create_index('idx_attack_name', 'kg_attack_types', ['name'])
    op.create_index('idx_vulnerability_cve', 'kg_vulnerabilities', ['cve_id'])
    op.create_index('idx_relationship_source', 'kg_entity_relationships', ['source_id'])
    op.create_index('idx_relationship_target', 'kg_entity_relationships', ['target_id'])

def downgrade():
    # 删除索引
    op.drop_index('idx_relationship_target', table_name='kg_entity_relationships')
    op.drop_index('idx_relationship_source', table_name='kg_entity_relationships')
    op.drop_index('idx_vulnerability_cve', table_name='kg_vulnerabilities')
    op.drop_index('idx_attack_name', table_name='kg_attack_types')
    op.drop_index('idx_entity_type', table_name='kg_entities')
    op.drop_index('idx_entity_name', table_name='kg_entities')
    
    # 删除表（按照依赖关系的相反顺序）
    op.drop_table('kg_entity_relationships')
    op.drop_table('kg_vulnerabilities')
    op.drop_table('kg_attack_types')
    op.drop_table('kg_entities')
    
    # 删除枚举类型
    op.execute('DROP TYPE IF EXISTS entity_status')
    op.execute('DROP TYPE IF EXISTS attack_status')
    op.execute('DROP TYPE IF EXISTS vulnerability_status')
    op.execute('DROP TYPE IF EXISTS vulnerability_severity')