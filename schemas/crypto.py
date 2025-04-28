from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CryptoAssetBase(BaseModel):
    name: str
    symbol: str
    description: Optional[str] = None
    website: Optional[str] = None
    explorer: Optional[str] = None
    research: Optional[str] = None
    social_links: Optional[dict] = None
    type: Optional[str] = None
    platform: Optional[str] = None
    contract_address: Optional[str] = None
    slug: str
    num_market_pairs: int
    date_added: datetime
    tags: List[str]
    max_supply: Optional[float]
    circulating_supply: float
    total_supply: float
    infinite_supply: bool
    cmc_rank: int
    self_reported_circulating_supply: Optional[float]
    self_reported_market_cap: Optional[float]
    tvl_ratio: Optional[float]

class CryptoAssetCreate(CryptoAssetBase):
    id: str

class CryptoAsset(CryptoAssetBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CryptoLiveDataBase(BaseModel):
    asset_id: str
    price_usd: float
    price_btc: Optional[float] = None
    volume_24h: Optional[float] = None
    market_cap: Optional[float] = None
    total_supply: Optional[float] = None
    circulating_supply: Optional[float] = None
    max_supply: Optional[float] = None
    price_change_24h: Optional[float] = None
    price_change_7d: Optional[float] = None
    price_change_30d: Optional[float] = None
    price_change_1y: Optional[float] = None
    market_cap_change_24h: Optional[float] = None
    market_cap_change_7d: Optional[float] = None
    market_cap_change_30d: Optional[float] = None
    market_cap_change_1y: Optional[float] = None
    volume_change_24h: Optional[float] = None
    volume_change_7d: Optional[float] = None
    volume_change_30d: Optional[float] = None
    volume_change_1y: Optional[float] = None

class CryptoLiveData(CryptoLiveDataBase):
    last_updated: datetime

    class Config:
        orm_mode = True

class CryptoHistoricalDataBase(BaseModel):
    asset_id: str
    timestamp: datetime
    interval: str
    price_usd: float
    price_btc: Optional[float] = None
    volume_24h: Optional[float] = None
    market_cap: Optional[float] = None
    total_supply: Optional[float] = None
    circulating_supply: Optional[float] = None
    max_supply: Optional[float] = None
    price_change_24h: Optional[float] = None
    price_change_7d: Optional[float] = None
    price_change_30d: Optional[float] = None
    price_change_1y: Optional[float] = None
    market_cap_change_24h: Optional[float] = None
    market_cap_change_7d: Optional[float] = None
    market_cap_change_30d: Optional[float] = None
    market_cap_change_1y: Optional[float] = None
    volume_change_24h: Optional[float] = None
    volume_change_7d: Optional[float] = None
    volume_change_30d: Optional[float] = None
    volume_change_1y: Optional[float] = None

class CryptoHistoricalData(CryptoHistoricalDataBase):
    id: int

    class Config:
        orm_mode = True 