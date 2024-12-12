from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from ..models.alert_rules import MetricType, ComparisonOperator

class AlertRuleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    metric_type: MetricType
    operator: ComparisonOperator
    threshold: float
    duration: int = Field(0, ge=0)  # 持续时间不能为负数
    enabled: bool = True
    notify_methods: List[str]
    cooldown: int = Field(300, ge=0)  # 冷却时间不能为负数

class AlertRuleCreate(AlertRuleBase):
    pass

class AlertRuleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    metric_type: Optional[MetricType] = None
    operator: Optional[ComparisonOperator] = None
    threshold: Optional[float] = None
    duration: Optional[int] = Field(None, ge=0)
    enabled: Optional[bool] = None
    notify_methods: Optional[List[str]] = None
    cooldown: Optional[int] = Field(None, ge=0)

class AlertRuleInDB(AlertRuleBase):
    id: int
    user_id: int
    last_triggered: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AlertRuleResponse(AlertRuleInDB):
    pass

class AlertRuleList(BaseModel):
    total: int
    items: List[AlertRuleResponse] 