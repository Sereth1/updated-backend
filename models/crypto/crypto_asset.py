from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from database import Base

class CryptoAsset(Base):
    __tablename__ = "crypto_assets"

    id = Column(String, primary_key=True)  # CoinCap's asset ID
    name = Column(String)
    symbol = Column(String, unique=True)
    slug = Column(String)
    num_market_pairs = Column(Integer)
    date_added = Column(DateTime)
    tags = Column(JSON)  # List of strings
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
    price_usd = Column(Float, nullable=True)
    market_cap = Column(Float, nullable=True)
    volume_24h = Column(Float, nullable=True)
    percent_change_24h = Column(Float, nullable=True)
    # removed vwap_24hr, explorer, created_at, updated_at 