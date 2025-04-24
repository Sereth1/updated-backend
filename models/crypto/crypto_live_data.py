from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class CryptoLiveData(Base):
    __tablename__ = "crypto_live_data"

    id = Column(String, primary_key=True)  # asset_id + timestamp
    asset_id = Column(String, ForeignKey("crypto_assets.id"))
    price_usd = Column(Float)
    market_cap_usd = Column(Float)
    volume_usd_24hr = Column(Float)
    change_percent_24hr = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) 