from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey
from database import Base
from datetime import datetime

class UserCurrentLocation(Base):
    __tablename__ = "user_current_location"

    user_id: Mapped[str] = mapped_column(String, ForeignKey("user.id"), primary_key=True)
    ip: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    region: Mapped[str] = mapped_column(String)
    timezone: Mapped[str] = mapped_column(String)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
