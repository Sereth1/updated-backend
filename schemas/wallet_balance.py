from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from decimal import Decimal

class WalletBalanceOut(BaseModel):
    id: UUID
    asset_id: str
    balance: Decimal

    class Config:
        orm_mode = True
