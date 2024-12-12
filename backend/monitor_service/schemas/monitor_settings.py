from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

class MonitorSettingsBase(BaseModel):
    """监控设置基础模型"""
    login_alert: bool = True
    operation_alert: bool = False
    security_alert: bool = True
    notify_methods: List[str] = ["web"]

class MonitorSettingsCreate(MonitorSettingsBase):
    """创建监控设置的请求模型"""
    pass

class MonitorSettingsUpdate(MonitorSettingsBase):
    """更新监控设置的请求模型"""
    pass

class MonitorSettingsResponse(MonitorSettingsBase):
    """监控设置的响应模型"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) 