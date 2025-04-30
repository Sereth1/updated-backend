from sqlalchemy import Column, String, DateTime, ForeignKey,Mapped,mapped_column
from database import Base

class UserLocationLog(Base):
    __tablename__ = "user_location_logs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    ip = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    region = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)   # ✅ match DB column name
    updated_at = Column(DateTime, nullable=False)   # ✅ match DB column name
    timezone: Mapped[str] = mapped_column(String)
