from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CryptoLiveDataBase(BaseModel):
    asset_id: str
    price_usd: float
    volume_24h: float
    volume_change_24h: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    percent_change_30d: float
    percent_change_60d: float
    percent_change_90d: float
    market_cap: float
    market_cap_dominance: float
    fully_diluted_market_cap: float
    tvl: Optional[float] = None

class CryptoLiveDataCreate(CryptoLiveDataBase):
    id: str

class CryptoLiveDataOut(CryptoLiveDataBase):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True 