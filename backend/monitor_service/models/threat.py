from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum as SQLEnum
from backend.monitor_service.database import Base

class ThreatLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    WARNING = "warning"
    CRITICAL = "critical"

class ThreatEvent(Base):
    __tablename__ = "threat_events"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(SQLEnum(ThreatLevel), nullable=False)
    type = Column(String, nullable=False)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_ip = Column(String)
    details = Column(JSON)
    status = Column(String, default="pending")  # pending, processing, resolved
    resolution = Column(String)
    resolved_at = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "level": self.level.value,
            "type": self.type,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "source_ip": self.source_ip,
            "details": self.details,
            "status": self.status,
            "resolution": self.resolution,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None
        } 