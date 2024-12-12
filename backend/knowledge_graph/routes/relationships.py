from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..database import get_db
from ..models.relationships import EntityRelationship, RelationshipStatus
from ..schemas.relationships import (
    Relationship,
    RelationshipCreate,
    RelationshipUpdate,
    PrerequisiteCreate,
    RelatedCreate
)
from ..core.deps import get_current_user
from ..core.logger import logger

router = APIRouter(prefix="/relationships", tags=["relationships"])

@router.post("", response_model=Relationship)
async def create_relationship(
    relationship: RelationshipCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建实体关系"""
    try:
        db_relationship = EntityRelationship(
            source_id=relationship.source_id,
            target_id=relationship.target_id,
            relationship_type=relationship.relationship_type,
            properties=relationship.properties
        )
        db.add(db_relationship)
        db.commit()
        db.refresh(db_relationship)
        return db_relationship
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的实体ID或关系已存在"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"创建关系失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建关系失败: {str(e)}"
        )

@router.get("", response_model=List[Relationship])
async def get_relationships(
    source_id: Optional[int] = None,
    target_id: Optional[int] = None,
    relationship_type: Optional[str] = None,
    status: Optional[RelationshipStatus] = RelationshipStatus.ACTIVE,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取实体关系列表"""
    query = db.query(EntityRelationship)
    
    if source_id is not None:
        query = query.filter(EntityRelationship.source_id == source_id)
    if target_id is not None:
        query = query.filter(EntityRelationship.target_id == target_id)
    if relationship_type is not None:
        query = query.filter(EntityRelationship.relationship_type == relationship_type)
    if status is not None:
        query = query.filter(EntityRelationship.status == status)
        
    relationships = query.offset(skip).limit(limit).all()
    return relationships

@router.get("/{relationship_id}", response_model=Relationship)
async def get_relationship(relationship_id: int, db: Session = Depends(get_db)):
    """获取实体关系详情"""
    relationship = db.query(EntityRelationship).filter(
        EntityRelationship.id == relationship_id
    ).first()
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="关系不存在"
        )
    return relationship

@router.put("/{relationship_id}", response_model=Relationship)
async def update_relationship(
    relationship_id: int,
    relationship_update: RelationshipUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """更新实体关系"""
    db_relationship = db.query(EntityRelationship).filter(
        EntityRelationship.id == relationship_id
    ).first()
    
    if not db_relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="关系不存在"
        )
    
    try:
        # 更新关系属性
        for field, value in relationship_update.dict(exclude_unset=True).items():
            setattr(db_relationship, field, value)
            
        db.commit()
        db.refresh(db_relationship)
        return db_relationship
    except Exception as e:
        db.rollback()
        logger.error(f"更新关系失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新关系失败: {str(e)}"
        )

@router.delete("/{relationship_id}")
async def delete_relationship(
    relationship_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除实体关系"""
    db_relationship = db.query(EntityRelationship).filter(
        EntityRelationship.id == relationship_id
    ).first()
    
    if not db_relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="关系不存在"
        )
    
    try:
        db.delete(db_relationship)
        db.commit()
        return {"message": "关系已删除"}
    except Exception as e:
        db.rollback()
        logger.error(f"删除关系失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除关系失败: {str(e)}"
        )

@router.post("/prerequisites", response_model=dict)
async def create_prerequisite(
    prerequisite: PrerequisiteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建前置知识关系"""
    try:
        # 创建双向的前置知识关系
        db_relationship = EntityRelationship(
            source_id=prerequisite.entity_id,
            target_id=prerequisite.prerequisite_id,
            relationship_type="prerequisite"
        )
        db.add(db_relationship)
        db.commit()
        return {"message": "前置知识关系创建成功"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的实体ID或关系已存在"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"创建前置知识关系失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建前置知识关系失败: {str(e)}"
        )

@router.post("/related", response_model=dict)
async def create_related(
    related: RelatedCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建相关知识关系"""
    try:
        # 创建双向的相关知识关系
        db_relationship = EntityRelationship(
            source_id=related.entity_id,
            target_id=related.related_id,
            relationship_type="related"
        )
        db.add(db_relationship)
        
        # 创建反向关系
        db_reverse_relationship = EntityRelationship(
            source_id=related.related_id,
            target_id=related.entity_id,
            relationship_type="related"
        )
        db.add(db_reverse_relationship)
        
        db.commit()
        return {"message": "相关知识关系创建成功"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的实体ID或关系已存在"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"创建相关知识关系失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建相关知识关系失败: {str(e)}"
        )