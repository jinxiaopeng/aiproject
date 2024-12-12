from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..database import get_db
from ..models.relationships import EntityRelationship
from ..schemas.entities import (
    Entity,
    EntityCreate,
    EntityUpdate,
    EntityWithRelations,
    EntityStatus,
    EntityType
)
from ..core.deps import get_current_user
from ..core.logger import logger

router = APIRouter(prefix="/entities", tags=["entities"])

@router.post("", response_model=Entity)
async def create_entity(
    entity: EntityCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建实体"""
    try:
        from ..models.relationships import Entity as EntityModel
        
        db_entity = EntityModel(
            name=entity.name,
            entity_type=entity.entity_type,
            description=entity.description,
            properties=entity.properties
        )
        db.add(db_entity)
        db.commit()
        db.refresh(db_entity)
        return db_entity
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="实体名称已存在"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"创建实体失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建实体失败: {str(e)}"
        )

@router.get("", response_model=List[Entity])
async def get_entities(
    name: Optional[str] = None,
    entity_type: Optional[EntityType] = None,
    status: Optional[EntityStatus] = EntityStatus.ACTIVE,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取实体列表"""
    from ..models.relationships import Entity as EntityModel
    
    query = db.query(EntityModel)
    
    if name:
        query = query.filter(EntityModel.name.ilike(f"%{name}%"))
    if entity_type:
        query = query.filter(EntityModel.entity_type == entity_type)
    if status:
        query = query.filter(EntityModel.status == status)
        
    entities = query.offset(skip).limit(limit).all()
    return entities

@router.get("/{entity_id}", response_model=EntityWithRelations)
async def get_entity(entity_id: int, db: Session = Depends(get_db)):
    """获取实体详情"""
    from ..models.relationships import Entity as EntityModel
    
    entity = db.query(EntityModel).filter(
        EntityModel.id == entity_id
    ).first()
    
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="实体不存在"
        )
    return entity

@router.put("/{entity_id}", response_model=Entity)
async def update_entity(
    entity_id: int,
    entity_update: EntityUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """更新实体"""
    from ..models.relationships import Entity as EntityModel
    
    db_entity = db.query(EntityModel).filter(
        EntityModel.id == entity_id
    ).first()
    
    if not db_entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="实体不存在"
        )
    
    try:
        # 更新实体属性
        for field, value in entity_update.dict(exclude_unset=True).items():
            setattr(db_entity, field, value)
            
        db.commit()
        db.refresh(db_entity)
        return db_entity
    except Exception as e:
        db.rollback()
        logger.error(f"更新实体失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新实体失败: {str(e)}"
        )

@router.delete("/{entity_id}")
async def delete_entity(
    entity_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除实体"""
    from ..models.relationships import Entity as EntityModel
    
    db_entity = db.query(EntityModel).filter(
        EntityModel.id == entity_id
    ).first()
    
    if not db_entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="实体不存在"
        )
    
    try:
        # 删除相关的关系
        db.query(EntityRelationship).filter(
            (EntityRelationship.source_id == entity_id) |
            (EntityRelationship.target_id == entity_id)
        ).delete(synchronize_session=False)
        
        # 删除实体
        db.delete(db_entity)
        db.commit()
        return {"message": "实体已删除"}
    except Exception as e:
        db.rollback()
        logger.error(f"删除实体失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除实体失败: {str(e)}"
        )

@router.get("/{entity_id}/relationships", response_model=List[EntityRelationship])
async def get_entity_relationships(
    entity_id: int,
    relationship_type: Optional[str] = None,
    direction: Optional[str] = Query(None, regex="^(incoming|outgoing|both)$"),
    db: Session = Depends(get_db)
):
    """获取实体的关系"""
    from ..models.relationships import Entity as EntityModel
    
    entity = db.query(EntityModel).filter(
        EntityModel.id == entity_id
    ).first()
    
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="实体不存在"
        )
    
    query = db.query(EntityRelationship)
    
    if direction == "incoming":
        query = query.filter(EntityRelationship.target_id == entity_id)
    elif direction == "outgoing":
        query = query.filter(EntityRelationship.source_id == entity_id)
    else:  # both
        query = query.filter(
            (EntityRelationship.source_id == entity_id) |
            (EntityRelationship.target_id == entity_id)
        )
    
    if relationship_type:
        query = query.filter(EntityRelationship.relationship_type == relationship_type)
        
    relationships = query.all()
    return relationships