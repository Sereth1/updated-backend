from pydantic import BaseModel
from datetime import datetime

class CryptoLiveDataBase(BaseModel):
    asset_id: str
    price_usd: float
    market_cap_usd: float
    volume_usd_24hr: float
    change_percent_24hr: float

class CryptoLiveDataCreate(CryptoLiveDataBase):
    pass

class CryptoLiveDataOut(CryptoLiveDataBase):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True 