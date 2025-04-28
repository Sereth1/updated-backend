from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from database import Base

class CryptoAsset(Base):
    __tablename__ = "crypto_assets"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    symbol = Column(String, index=True)
    slug = Column(String, index=True)
    num_market_pairs = Column(Integer)
    date_added = Column(DateTime)
    tags = Column(JSON)
    max_supply = Column(Float, nullable=True)
    circulating_supply = Column(Float)
    total_supply = Column(Float)
    infinite_supply = Column(Boolean)
    platform = Column(String, nullable=True)
    cmc_rank = Column(Integer)
    self_reported_circulating_supply = Column(Float, nullable=True)
    self_reported_market_cap = Column(Float, nullable=True)
    tvl_ratio = Column(Float, nullable=True)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

class CryptoLiveData(Base):
    __tablename__ = "crypto_live_data"

    id = Column(String, primary_key=True, index=True)
    asset_id = Column(String, ForeignKey("crypto_assets.id"))
    price_usd = Column(Float)
    volume_24h = Column(Float)
    volume_change_24h = Column(Float)
    percent_change_1h = Column(Float)
    percent_change_24h = Column(Float)
    percent_change_7d = Column(Float)
    percent_change_30d = Column(Float)
    percent_change_60d = Column(Float)
    percent_change_90d = Column(Float)
    market_cap = Column(Float)
    market_cap_dominance = Column(Float)
    fully_diluted_market_cap = Column(Float)
    tvl = Column(Float, nullable=True)
    timestamp = Column(DateTime, server_default=func.now())

class CryptoHistoricalData(Base):
    __tablename__ = "crypto_historical_data"

    id = Column(String, primary_key=True, index=True)
    asset_id = Column(String, ForeignKey("crypto_assets.id"))
    price_usd = Column(Float)
    volume_24h = Column(Float)
    volume_change_24h = Column(Float)
    percent_change_1h = Column(Float)
    percent_change_24h = Column(Float)
    percent_change_7d = Column(Float)
    percent_change_30d = Column(Float)
    percent_change_60d = Column(Float)
    percent_change_90d = Column(Float)
    market_cap = Column(Float)
    market_cap_dominance = Column(Float)
    fully_diluted_market_cap = Column(Float)
    tvl = Column(Float, nullable=True)
    interval = Column(String)
    timestamp = Column(DateTime, server_default=func.now()) 