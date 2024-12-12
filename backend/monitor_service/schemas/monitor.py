from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..models.monitor import AlertType, AlertLevel, AlertStatus

class MonitorSettingsBase(BaseModel):
    login_alert: bool = True
    operation_alert: bool = False
    security_alert: bool = True
    notify_methods: List[str] = ["email", "web"]

class MonitorSettingsCreate(MonitorSettingsBase):
    user_id: int

class MonitorSettingsUpdate(MonitorSettingsBase):
    pass

class MonitorSettings(MonitorSettingsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MonitorAlertBase(BaseModel):
    user_id: int
    type: AlertType
    level: AlertLevel
    title: str
    content: str
    ip_address: Optional[str] = None

class MonitorAlertCreate(MonitorAlertBase):
    pass

class MonitorAlertUpdate(BaseModel):
    status: AlertStatus
    handled_at: Optional[datetime] = None

class MonitorAlert(MonitorAlertBase):
    id: int
    status: AlertStatus
    created_at: datetime
    updated_at: datetime
    handled_at: Optional[datetime]

    class Config:
        from_attributes = True 