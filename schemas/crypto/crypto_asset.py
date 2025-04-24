from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CryptoAssetBase(BaseModel):
    id: str
    rank: int
    symbol: str
    name: str
    supply: float
    max_supply: Optional[float] = None
    market_cap_usd: float
    volume_usd_24hr: float
    price_usd: float
    change_percent_24hr: float
    vwap_24hr: Optional[float] = None
    explorer: Optional[str] = None

class CryptoAssetCreate(CryptoAssetBase):
    pass

class CryptoAssetOut(CryptoAssetBase):
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 