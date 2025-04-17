from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from decimal import Decimal

from database import get_session
from models.wallet import Wallet, WalletBalance
from models.asset import Asset
from schemas.wallet import WalletOut
from schemas.wallet_balance import WalletBalanceOut
from schemas.asset import AssetOut

router = APIRouter()
@router.post("/wallet", response_model=WalletOut)
async def create_wallet(user_id: str, db: AsyncSession = Depends(get_session)):
    # Check if wallet already exists
    existing = await db.execute(select(Wallet).where(Wallet.user_id == user_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Wallet already exists")

    wallet = Wallet(user_id=user_id)
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)
    return wallet

@router.get("/wallet/{user_id}", response_model=WalletOut)
async def get_wallet(user_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Wallet).where(Wallet.user_id == user_id))
    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@router.post("/wallet/deposit", response_model=WalletBalanceOut)
async def deposit(
    user_id: str,
    asset_id: str,
    amount: Decimal,
    db: AsyncSession = Depends(get_session)
):
    # ✅ Check asset exists
    asset_result = await db.execute(select(Asset).where(Asset.id == asset_id))
    asset = asset_result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=400, detail="Asset does not exist")

    # ✅ Prevent negative/zero deposit
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be greater than zero")

    # ✅ Find wallet
    wallet_result = await db.execute(select(Wallet).where(Wallet.user_id == user_id))
    wallet = wallet_result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    # ✅ Check if balance already exists
    balance_result = await db.execute(
        select(WalletBalance).where(
            WalletBalance.wallet_id == wallet.id,
            WalletBalance.asset_id == asset_id
        )
    )
    balance = balance_result.scalar_one_or_none()

    if balance:
        balance.balance += amount
    else:
        balance = WalletBalance(wallet_id=wallet.id, asset_id=asset_id, balance=amount)
        db.add(balance)

    await db.commit()
    await db.refresh(balance)
    return balance

@router.get("/assets", response_model=list[AssetOut])
async def list_assets(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Asset))
    return result.scalars().all()
