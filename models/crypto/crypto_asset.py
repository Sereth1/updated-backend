from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.sql import func
from database import Base

class CryptoAsset(Base):
    __tablename__ = "crypto_assets"

    id = Column(String, primary_key=True)  # CoinCap's asset ID
    rank = Column(Integer)
    symbol = Column(String, unique=True)
    name = Column(String)
    supply = Column(Float)
    max_supply = Column(Float, nullable=True)
    market_cap_usd = Column(Float)
    volume_usd_24hr = Column(Float)
    price_usd = Column(Float)
    change_percent_24hr = Column(Float)
    vwap_24hr = Column(Float, nullable=True)
    explorer = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 