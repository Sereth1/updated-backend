from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CryptoLiveDataBase(BaseModel):
    asset_id: str
    price_usd: float
    volume_24h: float
    volume_change_24h: Optional[float] = None
    percent_change_1h: Optional[float] = None
    percent_change_24h: float
    percent_change_7d: Optional[float] = None
    percent_change_30d: Optional[float] = None
    percent_change_60d: Optional[float] = None
    percent_change_90d: Optional[float] = None
    market_cap: Optional[float] = None
    market_cap_dominance: Optional[float] = None
    fully_diluted_market_cap: Optional[float] = None
    tvl: Optional[float] = None
    timestamp: Optional[datetime] = None

class CryptoLiveDataCreate(CryptoLiveDataBase):
    id: str

class CryptoLiveDataOut(CryptoLiveDataBase):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True 