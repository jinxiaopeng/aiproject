from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class RelationshipType(str, Enum):
    PREREQUISITE = "prerequisite"
    RELATED = "related"
    INCLUDES = "includes"
    LEADS_TO = "leads_to"
    MITIGATES = "mitigates"
    EXPLOITS = "exploits"
    AFFECTS = "affects"

class RelationshipStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"

class RelationshipBase(BaseModel):
    source_id: int = Field(..., description="源实体ID")
    target_id: int = Field(..., description="目标实体ID")
    relationship_type: RelationshipType = Field(..., description="关系类型")
    properties: Optional[Dict[str, Any]] = Field(None, description="关系属性")

class RelationshipCreate(RelationshipBase):
    pass

class RelationshipUpdate(BaseModel):
    relationship_type: Optional[RelationshipType] = None
    properties: Optional[Dict[str, Any]] = None
    status: Optional[RelationshipStatus] = None

class RelationshipInDB(RelationshipBase):
    id: int
    status: RelationshipStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Relationship(RelationshipInDB):
    pass

class PrerequisiteCreate(BaseModel):
    entity_id: int = Field(..., description="实体ID")
    prerequisite_id: int = Field(..., description="前置知识ID")

class RelatedCreate(BaseModel):
    entity_id: int = Field(..., description="实体ID")
    related_id: int = Field(..., description="相关知识ID") 