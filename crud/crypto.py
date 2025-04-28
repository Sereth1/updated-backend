from sqlalchemy.orm import Session
from models.crypto import CryptoAsset, CryptoLiveData, CryptoHistoricalData
from schemas.crypto import CryptoAssetCreate, CryptoLiveDataBase, CryptoHistoricalDataBase
from typing import List, Optional
from datetime import datetime

def get_crypto_asset(db: Session, asset_id: str) -> Optional[CryptoAsset]:
    return db.query(CryptoAsset).filter(CryptoAsset.id == asset_id).first()

def get_crypto_assets(db: Session, skip: int = 0, limit: int = 100) -> List[CryptoAsset]:
    return db.query(CryptoAsset).offset(skip).limit(limit).all()

def create_crypto_asset(db: Session, asset: CryptoAssetCreate) -> CryptoAsset:
    db_asset = CryptoAsset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def update_crypto_asset(db: Session, asset_id: str, asset_data: dict) -> Optional[CryptoAsset]:
    db_asset = get_crypto_asset(db, asset_id)
    if db_asset:
        for key, value in asset_data.items():
            setattr(db_asset, key, value)
        db.commit()
        db.refresh(db_asset)
    return db_asset

def get_live_data(db: Session, asset_id: str) -> Optional[CryptoLiveData]:
    return db.query(CryptoLiveData).filter(CryptoLiveData.asset_id == asset_id).first()

def create_live_data(db: Session, live_data: CryptoLiveDataBase) -> CryptoLiveData:
    db_live_data = CryptoLiveData(**live_data.dict())
    db.add(db_live_data)
    db.commit()
    db.refresh(db_live_data)
    return db_live_data

def get_historical_data(
    db: Session,
    asset_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    interval: Optional[str] = None
) -> List[CryptoHistoricalData]:
    query = db.query(CryptoHistoricalData).filter(CryptoHistoricalData.asset_id == asset_id)
    
    if start_time:
        query = query.filter(CryptoHistoricalData.timestamp >= start_time)
    if end_time:
        query = query.filter(CryptoHistoricalData.timestamp <= end_time)
    if interval:
        query = query.filter(CryptoHistoricalData.interval == interval)
        
    return query.order_by(CryptoHistoricalData.timestamp).all()

def create_historical_data(db: Session, historical_data: CryptoHistoricalDataBase) -> CryptoHistoricalData:
    db_historical_data = CryptoHistoricalData(**historical_data.dict())
    db.add(db_historical_data)
    db.commit()
    db.refresh(db_historical_data)
    return db_historical_data 