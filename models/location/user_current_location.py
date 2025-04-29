from sqlalchemy import Column, String, DateTime, ForeignKey
from database import Base
from datetime import datetime
from typing import Optional

class UserCurrentLocation(Base):
    __tablename__ = "user_current_location"

    user_id = Column(String, ForeignKey("user.id"), primary_key=True)
    ip = Column(String)
    country = Column(String)
    city = Column(String)
    region = Column(String)
    timezone: Optional[str]
    updated_at = Column(DateTime, default=datetime.utcnow)
