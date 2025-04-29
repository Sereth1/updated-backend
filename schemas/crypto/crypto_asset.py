from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CryptoAssetBase(BaseModel):
    name: Optional[str] = None
    symbol: Optional[str] = None
    slug: Optional[str] = None
    num_market_pairs: Optional[int] = None
    date_added: Optional[datetime] = None
    tags: Optional[List[str]] = None
    max_supply: Optional[float] = None
    circulating_supply: Optional[float] = None
    total_supply: Optional[float] = None
    infinite_supply: Optional[bool] = None
    platform: Optional[str] = None
    cmc_rank: Optional[int] = None
    self_reported_circulating_supply: Optional[float] = None
    self_reported_market_cap: Optional[float] = None
    tvl_ratio: Optional[float] = None
    last_updated: Optional[datetime] = None
    price_usd: Optional[float] = None
    market_cap: Optional[float] = None
    volume_24h: Optional[float] = None
    percent_change_24h: Optional[float] = None

class CryptoAssetCreate(CryptoAssetBase):
    id: str

class CryptoAssetOut(CryptoAssetBase):
    id: str
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True 