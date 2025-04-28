from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.crypto import CryptoAsset, CryptoLiveData, CryptoHistoricalData
from schemas.crypto import CryptoAssetCreate, CryptoAssetResponse, CryptoLiveDataResponse, CryptoHistoricalDataResponse
from typing import List
from datetime import datetime, timedelta
import uuid

router = APIRouter()

@router.post("/assets", response_model=CryptoAssetResponse)
async def create_crypto_asset(asset: CryptoAssetCreate, db: Session = Depends(get_db)):
    db_asset = CryptoAsset(
        id=str(uuid.uuid4()),
        name=asset.name,
        symbol=asset.symbol,
        slug=asset.slug,
        num_market_pairs=asset.num_market_pairs,
        date_added=asset.date_added,
        tags=asset.tags,
        max_supply=asset.max_supply,
        circulating_supply=asset.circulating_supply,
        total_supply=asset.total_supply,
        infinite_supply=asset.infinite_supply,
        platform=asset.platform,
        cmc_rank=asset.cmc_rank,
        self_reported_circulating_supply=asset.self_reported_circulating_supply,
        self_reported_market_cap=asset.self_reported_market_cap,
        tvl_ratio=asset.tvl_ratio,
        last_updated=datetime.utcnow()
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/assets", response_model=List[CryptoAssetResponse])
async def get_crypto_assets(db: Session = Depends(get_db)):
    return db.query(CryptoAsset).all()

@router.get("/assets/{asset_id}", response_model=CryptoAssetResponse)
async def get_crypto_asset(asset_id: str, db: Session = Depends(get_db)):
    asset = db.query(CryptoAsset).filter(CryptoAsset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.post("/live-data", response_model=CryptoLiveDataResponse)
async def create_crypto_live_data(data: dict, db: Session = Depends(get_db)):
    db_data = CryptoLiveData(
        id=str(uuid.uuid4()),
        asset_id=data["asset_id"],
        price_usd=data["price_usd"],
        volume_24h=data["volume_24h"],
        volume_change_24h=data["volume_change_24h"],
        percent_change_1h=data["percent_change_1h"],
        percent_change_24h=data["percent_change_24h"],
        percent_change_7d=data["percent_change_7d"],
        percent_change_30d=data["percent_change_30d"],
        percent_change_60d=data["percent_change_60d"],
        percent_change_90d=data["percent_change_90d"],
        market_cap=data["market_cap"],
        market_cap_dominance=data["market_cap_dominance"],
        fully_diluted_market_cap=data["fully_diluted_market_cap"],
        tvl=data["tvl"],
        timestamp=datetime.utcnow()
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@router.get("/live-data/{asset_id}", response_model=CryptoLiveDataResponse)
async def get_latest_crypto_data(asset_id: str, db: Session = Depends(get_db)):
    data = db.query(CryptoLiveData).filter(CryptoLiveData.asset_id == asset_id).order_by(CryptoLiveData.timestamp.desc()).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@router.post("/historical-data", response_model=CryptoHistoricalDataResponse)
async def create_crypto_historical_data(data: dict, db: Session = Depends(get_db)):
    db_data = CryptoHistoricalData(
        id=str(uuid.uuid4()),
        asset_id=data["asset_id"],
        price_usd=data["price_usd"],
        volume_24h=data["volume_24h"],
        volume_change_24h=data["volume_change_24h"],
        percent_change_1h=data["percent_change_1h"],
        percent_change_24h=data["percent_change_24h"],
        percent_change_7d=data["percent_change_7d"],
        percent_change_30d=data["percent_change_30d"],
        percent_change_60d=data["percent_change_60d"],
        percent_change_90d=data["percent_change_90d"],
        market_cap=data["market_cap"],
        market_cap_dominance=data["market_cap_dominance"],
        fully_diluted_market_cap=data["fully_diluted_market_cap"],
        tvl=data["tvl"],
        timestamp=data["timestamp"],
        interval=data["interval"]
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@router.get("/historical-data/{asset_id}", response_model=List[CryptoHistoricalDataResponse])
async def get_crypto_historical_data(
    asset_id: str,
    start_date: datetime,
    end_date: datetime,
    interval: str = "24h",
    db: Session = Depends(get_db)
):
    data = db.query(CryptoHistoricalData).filter(
        CryptoHistoricalData.asset_id == asset_id,
        CryptoHistoricalData.timestamp >= start_date,
        CryptoHistoricalData.timestamp <= end_date,
        CryptoHistoricalData.interval == interval
    ).order_by(CryptoHistoricalData.timestamp.asc()).all()
    return data 