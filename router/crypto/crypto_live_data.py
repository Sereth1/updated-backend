from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from models.crypto import CryptoLiveData
from schemas.crypto import CryptoLiveDataCreate, CryptoLiveDataOut
from typing import List
import uuid

router = APIRouter()

@router.post("/live-data", response_model=CryptoLiveDataOut)
async def create_crypto_live_data(data: CryptoLiveDataCreate, db: AsyncSession = Depends(get_session)):
    db_data = CryptoLiveData(
        id=str(uuid.uuid4()),
        asset_id=data.asset_id,
        price_usd=data.price_usd,
        volume_24h=data.volume_24h,
        volume_change_24h=data.volume_change_24h,
        percent_change_1h=data.percent_change_1h,
        percent_change_24h=data.percent_change_24h,
        percent_change_7d=data.percent_change_7d,
        percent_change_30d=data.percent_change_30d,
        percent_change_60d=data.percent_change_60d,
        percent_change_90d=data.percent_change_90d,
        market_cap=data.market_cap,
        market_cap_dominance=data.market_cap_dominance,
        fully_diluted_market_cap=data.fully_diluted_market_cap,
        tvl=data.tvl
    )
    db.add(db_data)
    await db.commit()
    await db.refresh(db_data)
    return db_data 