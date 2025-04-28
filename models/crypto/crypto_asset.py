from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.sql import func
from database import Base

class CryptoAsset(Base):
    __tablename__ = "crypto_assets"

    id = Column(String, primary_key=True)  # CoinCap's asset ID
    cmc_rank = Column(Integer)
    symbol = Column(String, unique=True)
    name = Column(String)
    supply = Column(Float)
    max_supply = Column(Float, nullable=True)
    market_cap = Column(Float)
    volume_24h = Column(Float)
    price_usd = Column(Float)
    percent_change_24h = Column(Float)
    # removed vwap_24hr, explorer, created_at, updated_at 