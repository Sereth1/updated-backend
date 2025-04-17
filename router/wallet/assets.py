from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_session
from models.wallet.asset import Asset
from schemas.wallet.asset import AssetOut

router = APIRouter()

@router.get("/assets", response_model=list[AssetOut])
async def get_assets(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Asset))
    return result.scalars().all()
