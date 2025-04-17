from pydantic import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime
from .wallet_balance import WalletBalanceOut

class WalletOut(BaseModel):
    id: UUID
    user_id: str
    created_at: datetime
    balances: List[WalletBalanceOut] = []

    class Config:
        orm_mode = True
