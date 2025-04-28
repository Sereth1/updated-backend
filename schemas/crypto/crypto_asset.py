from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CryptoAssetBase(BaseModel):
    name: str
    symbol: str
    slug: str
    num_market_pairs: int
    date_added: datetime
    tags: List[str]
    max_supply: Optional[float] = None
    circulating_supply: float
    total_supply: float
    infinite_supply: bool
    platform: Optional[str] = None
    cmc_rank: int
    self_reported_circulating_supply: Optional[float] = None
    self_reported_market_cap: Optional[float] = None
    tvl_ratio: Optional[float] = None

class CryptoAssetCreate(CryptoAssetBase):
    id: str

class CryptoAssetOut(CryptoAssetBase):
    id: str
    last_updated: datetime

    class Config:
        from_attributes = True 