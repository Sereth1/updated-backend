from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class CryptoHistoricalData(Base):
    __tablename__ = "crypto_historical_data"

    id = Column(String, primary_key=True)  # asset_id + timestamp
    asset_id = Column(String, ForeignKey("crypto_assets.id"))
    price_usd = Column(Float)
    market_cap = Column(Float)
    volume_24h = Column(Float)
    volume_change_24h = Column(Float)
    percent_change_1h = Column(Float)
    percent_change_24h = Column(Float)
    percent_change_7d = Column(Float)
    percent_change_30d = Column(Float)
    percent_change_60d = Column(Float)
    percent_change_90d = Column(Float)
    market_cap_dominance = Column(Float)
    fully_diluted_market_cap = Column(Float)
    tvl = Column(Float)
    interval = Column(String)  # '1m', '5m', '1h', '1d', etc.
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) 