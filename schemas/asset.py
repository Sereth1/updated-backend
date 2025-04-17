from pydantic import BaseModel

class AssetOut(BaseModel):
    id: str
    symbol: str
    name: str
    type: str  # 'crypto' or 'fiat'

    class Config:
        orm_mode = True
