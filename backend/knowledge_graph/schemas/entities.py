from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class EntityType(str, Enum):
    CONCEPT = "concept"          # 概念
    ATTACK = "attack"           # 攻击方式
    VULNERABILITY = "vulnerability"  # 漏洞
    DEFENSE = "defense"         # 防御方法
    TOOL = "tool"              # 工具
    PROTOCOL = "protocol"       # 协议
    PLATFORM = "platform"       # 平台

class EntityStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"

class EntityBase(BaseModel):
    name: str = Field(..., description="实体名称")
    entity_type: EntityType = Field(..., description="实体类型")
    description: Optional[str] = Field(None, description="实体描述")
    properties: Optional[Dict[str, Any]] = Field(None, description="实体属性")

class EntityCreate(EntityBase):
    pass

class EntityUpdate(BaseModel):
    name: Optional[str] = None
    entity_type: Optional[EntityType] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    status: Optional[EntityStatus] = None

class EntityInDB(EntityBase):
    id: int
    status: EntityStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Entity(EntityInDB):
    pass

class EntityWithRelations(Entity):
    outgoing_relationships: List["Relationship"] = []
    incoming_relationships: List["Relationship"] = []

# 导入关系模型以避免循环导入
from .relationships import Relationship
EntityWithRelations.model_rebuild()  # 更新模型以包含关系 