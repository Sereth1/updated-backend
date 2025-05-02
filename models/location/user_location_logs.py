from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime

class UserLocationLog(Base):
    __tablename__ = "user_location_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))  # ✅ FIXED HERE
    ip: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    region: Mapped[str] = mapped_column(String)
    timezone: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

