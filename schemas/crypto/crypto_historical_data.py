from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class CryptoHistoricalDataBase(BaseModel):
    asset_id: str
    price_usd: float
    market_cap_usd: float
    volume_usd_24hr: float
    change_percent_24hr: float
    interval: Literal['1m', '5m', '1h', '1d']

class CryptoHistoricalDataCreate(CryptoHistoricalDataBase):
    pass

class CryptoHistoricalDataOut(CryptoHistoricalDataBase):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True 