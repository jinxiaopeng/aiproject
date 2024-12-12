from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MonitorSettingsBase(BaseModel):
    login_alert: bool = True
    operation_alert: bool = False
    security_alert: bool = True
    notify_methods: List[str] = ["email", "web"]

class MonitorSettingsCreate(MonitorSettingsBase):
    pass

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
    type: str
    level: str
    title: str
    content: str
    ip_address: Optional[str] = None

class MonitorAlertCreate(MonitorAlertBase):
    user_id: int

class MonitorAlertUpdate(BaseModel):
    status: str
    handled_at: Optional[datetime] = None

class MonitorAlert(MonitorAlertBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    handled_at: Optional[datetime]

    class Config:
        from_attributes = True

class MonitorStats(BaseModel):
    login_alerts: int = 0
    operation_alerts: int = 0
    security_alerts: int = 0 