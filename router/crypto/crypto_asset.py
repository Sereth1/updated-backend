from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import httpx
import asyncio
from datetime import datetime, timedelta
import os
from database import get_session, engine
from models.crypto import CryptoAsset
from models.crypto.crypto_live_data import CryptoLiveData
from models.crypto.crypto_historical_data import CryptoHistoricalData
from schemas.crypto import CryptoAssetCreate, CryptoAssetOut
from schemas.crypto.crypto_live_data import CryptoLiveDataOut
from schemas.crypto.crypto_historical_data import CryptoHistoricalDataOut
import uuid

router = APIRouter()

# CoinMarketCap API configuration
COINMARKETCAP_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
COINMARKETCAP_API_KEY = "d363f63a-c24f-46ab-be0f-e80bde08df62"
MAX_RETRIES = 3
RETRY_DELAY = 10
LIVE_UPDATE_INTERVAL = 3600  # 1 hour
HISTORICAL_UPDATE_INTERVAL = 43200  # 12 hours
CHECK_INTERVAL = 300  # 5 minutes

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        async with self.lock:
            now = datetime.utcnow()
            self.requests = [r for r in self.requests if (now - r).total_seconds() < self.time_window]
            
            if len(self.requests) >= self.max_requests:
                wait_time = self.time_window - (now - self.requests[0]).total_seconds()
                if wait_time > 0:
                    print(f"[RateLimiter] Sleeping for {wait_time:.2f} seconds due to limit.")
                    await asyncio.sleep(wait_time)
                self.requests.pop(0)
            
            self.requests.append(now)

# Initialize rate limiter (30 requests per minute - CoinMarketCap's free tier limit)
rate_limiter = RateLimiter(max_requests=30, time_window=60)

async def fetch_cmc_data_with_retry():
    if not COINMARKETCAP_API_KEY:
        raise HTTPException(status_code=500, detail="CoinMarketCap API key not configured")
        
    headers = {
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY,
        "Accept": "application/json"
    }
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            await rate_limiter.acquire()
            async with httpx.AsyncClient(timeout=30.0) as client:
                print(f"[Retry {attempt}] Fetching CoinMarketCap data...")
                response = await client.get(
                    COINMARKETCAP_API_URL,
                    headers=headers,
                    params={"limit": 5000, "convert": "USD"}
                )
                
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", RETRY_DELAY * attempt))
                    print(f"[Retry {attempt}] 429 Too Many Requests. Sleeping for {retry_after}s.")
                    await asyncio.sleep(retry_after)
                    continue
                
                if response.status_code != 200:
                    print(f"[Retry {attempt}] Failed with status: {response.status_code}")
                    raise HTTPException(status_code=response.status_code, detail="Failed to fetch CoinMarketCap data")
                
                data = response.json()["data"]
                print(f"Fetched data for {len(data)} cryptocurrencies")
                return data
                
        except httpx.RequestError as e:
            print(f"[Retry {attempt}] Network error: {str(e)}")
            if attempt < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY * attempt)
            else:
                raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
    
    raise HTTPException(status_code=500, detail="Failed to fetch CoinMarketCap data after retries")

async def ensure_asset_exists(db: AsyncSession, asset_data: dict):
    """Ensure the asset exists in the database before saving its data."""
    try:
        quote = asset_data["quote"]["USD"]
        
        # First check if the asset exists
        result = await db.execute(
            select(CryptoAsset).where(CryptoAsset.id == asset_data["symbol"])
        )
        existing_asset = result.scalar_one_or_none()
        
        if existing_asset:
            # Update existing asset
            existing_asset.cmc_rank = int(asset_data["cmc_rank"])
            existing_asset.symbol = asset_data["symbol"]
            existing_asset.name = asset_data["name"]
            existing_asset.supply = float(asset_data["circulating_supply"])
            existing_asset.max_supply = float(asset_data["max_supply"]) if asset_data["max_supply"] else None
            existing_asset.market_cap = float(quote["market_cap"])
            existing_asset.volume_24h = float(quote["volume_24h"])
            existing_asset.price_usd = float(quote["price"])
            existing_asset.percent_change_24h = float(quote["percent_change_24h"])
            await db.commit()
            print(f"Updated existing asset: {asset_data['symbol']}")
        else:
            # Create new asset
            new_asset = CryptoAsset(
                id=asset_data["symbol"],
                cmc_rank=int(asset_data["cmc_rank"]),
                symbol=asset_data["symbol"],
                name=asset_data["name"],
                supply=float(asset_data["circulating_supply"]),
                max_supply=float(asset_data["max_supply"]) if asset_data["max_supply"] else None,
                market_cap=float(quote["market_cap"]),
                volume_24h=float(quote["volume_24h"]),
                price_usd=float(quote["price"]),
                percent_change_24h=float(quote["percent_change_24h"])
            )
            db.add(new_asset)
            await db.commit()
            print(f"Created new asset: {asset_data['symbol']}")
            
    except Exception as e:
        await db.rollback()
        print(f"Error ensuring asset exists for {asset_data['symbol']}: {str(e)}")
        raise

async def update_live_data(db: AsyncSession):
    try:
        assets_data = await fetch_cmc_data_with_retry()
        current_time = datetime.utcnow()
        success_count = 0
        error_count = 0
        
        for asset_data in assets_data:
            try:
                # First ensure the asset exists
                await ensure_asset_exists(db, asset_data)
                
                quote = asset_data["quote"]["USD"]
                
                # Create new live data entry
                live_data = CryptoLiveData(
                    id=f"{asset_data['symbol']}_{current_time.strftime('%Y%m%d_%H%M%S')}",
                    asset_id=asset_data["symbol"],
                    price_usd=float(quote["price"]),
                    market_cap=float(quote["market_cap"]),
                    volume_24h=float(quote["volume_24h"]),
                    volume_change_24h=float(quote["volume_change_24h"]) if "volume_change_24h" in quote else None,
                    percent_change_1h=float(quote["percent_change_1h"]) if "percent_change_1h" in quote else None,
                    percent_change_24h=float(quote["percent_change_24h"]),
                    percent_change_7d=float(quote["percent_change_7d"]) if "percent_change_7d" in quote else None,
                    percent_change_30d=float(quote["percent_change_30d"]) if "percent_change_30d" in quote else None,
                    percent_change_60d=float(quote["percent_change_60d"]) if "percent_change_60d" in quote else None,
                    percent_change_90d=float(quote["percent_change_90d"]) if "percent_change_90d" in quote else None,
                    market_cap_dominance=float(quote["market_cap_dominance"]) if "market_cap_dominance" in quote else None,
                    fully_diluted_market_cap=float(quote["fully_diluted_market_cap"]) if "fully_diluted_market_cap" in quote else None,
                    tvl=float(quote["tvl"]) if "tvl" in quote else None,
                    timestamp=current_time
                )
                
                # Add the new live data
                db.add(live_data)
                success_count += 1
                
            except Exception as e:
                error_count += 1
                print(f"Error processing asset {asset_data['symbol']}: {str(e)}")
                continue
        
        # Commit all changes at once
        await db.commit()
        print(f"[{current_time}] Successfully updated live data for {success_count}/{len(assets_data)} assets. Errors: {error_count}")
        
    except Exception as e:
        await db.rollback()
        print(f"[{datetime.utcnow()}] Error updating live data: {str(e)}")
        raise

async def update_historical_data(db: AsyncSession):
    try:
        assets_data = await fetch_cmc_data_with_retry()
        current_time = datetime.utcnow()
        success_count = 0
        
        for asset_data in assets_data:
            try:
                # First ensure the asset exists
                await ensure_asset_exists(db, asset_data)
                
                quote = asset_data["quote"]["USD"]
                historical_data_id = f"{asset_data['symbol']}_{current_time.strftime('%Y%m%d_%H%M%S')}"
                
                # Check if historical data already exists for this time period
                result = await db.execute(
                    select(CryptoHistoricalData)
                    .where(
                        CryptoHistoricalData.asset_id == asset_data["symbol"],
                        CryptoHistoricalData.timestamp >= current_time - timedelta(hours=24),
                        CryptoHistoricalData.interval == "24h"
                    )
                )
                existing_data = result.scalar_one_or_none()
                
                if not existing_data:
                    historical_data = CryptoHistoricalData(
                        id=historical_data_id,
                        asset_id=asset_data["symbol"],
                        price_usd=float(quote["price"]),
                        market_cap=float(quote["market_cap"]),
                        volume_24h=float(quote["volume_24h"]),
                        volume_change_24h=float(quote["volume_change_24h"]) if "volume_change_24h" in quote else None,
                        percent_change_1h=float(quote["percent_change_1h"]) if "percent_change_1h" in quote else None,
                        percent_change_24h=float(quote["percent_change_24h"]),
                        percent_change_7d=float(quote["percent_change_7d"]) if "percent_change_7d" in quote else None,
                        percent_change_30d=float(quote["percent_change_30d"]) if "percent_change_30d" in quote else None,
                        percent_change_60d=float(quote["percent_change_60d"]) if "percent_change_60d" in quote else None,
                        percent_change_90d=float(quote["percent_change_90d"]) if "percent_change_90d" in quote else None,
                        market_cap_dominance=float(quote["market_cap_dominance"]) if "market_cap_dominance" in quote else None,
                        fully_diluted_market_cap=float(quote["fully_diluted_market_cap"]) if "fully_diluted_market_cap" in quote else None,
                        tvl=float(quote["tvl"]) if "tvl" in quote else None,
                        interval="24h",
                        timestamp=current_time
                    )
                    db.add(historical_data)
                    success_count += 1
            except Exception as e:
                print(f"Error processing asset {asset_data['symbol']}: {str(e)}")
                continue
        
        await db.commit()
        print(f"Successfully updated historical data for {success_count}/{len(assets_data)} assets at {current_time}")
    except Exception as e:
        await db.rollback()
        print(f"Error updating historical data: {str(e)}")
        raise

async def start_data_updates():
    # Create a single session for the entire update cycle
    async with AsyncSession(engine, expire_on_commit=False) as db:
        last_live_update = datetime.utcnow()
        last_historical_update = datetime.utcnow()
        
        while True:
            try:
                current_time = datetime.utcnow()
                
                # Check if it's time for live update
                if (current_time - last_live_update).total_seconds() >= LIVE_UPDATE_INTERVAL:
                    print(f"[{current_time}] Starting live data update...")
                    await update_live_data(db)
                    last_live_update = current_time
                    print(f"[{current_time}] Live data update completed. Next update in {LIVE_UPDATE_INTERVAL} seconds")
                
                # Check if it's time for historical update (every hour)
                if (current_time - last_historical_update).total_seconds() >= HISTORICAL_UPDATE_INTERVAL:
                    print(f"[{current_time}] Starting historical data update...")
                    await update_historical_data(db)
                    last_historical_update = current_time
                    print(f"[{current_time}] Historical data update completed. Next update in {HISTORICAL_UPDATE_INTERVAL/60} minutes")
                
                # Sleep for CHECK_INTERVAL seconds before checking again
                await asyncio.sleep(CHECK_INTERVAL)
                
            except Exception as e:
                print(f"[{datetime.utcnow()}] Error in data update cycle: {str(e)}")
                await db.rollback()
                print(f"[{datetime.utcnow()}] Sleeping for {CHECK_INTERVAL} seconds before retrying...")
                await asyncio.sleep(CHECK_INTERVAL)

@router.on_event("startup")
async def startup_event():
    asyncio.create_task(start_data_updates())

@router.get("/live", response_model=List[CryptoLiveDataOut])
async def get_live_data(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(CryptoLiveData)
        .order_by(CryptoLiveData.timestamp.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.get("/historical", response_model=List[CryptoHistoricalDataOut])
async def get_historical_data(interval: str = "1h", skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(CryptoHistoricalData)
        .where(CryptoHistoricalData.interval == interval)
        .order_by(CryptoHistoricalData.timestamp.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.get("/historical/{asset_id}", response_model=List[CryptoHistoricalDataOut])
async def get_asset_historical_data(asset_id: str, interval: str = "1h", skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(CryptoHistoricalData)
        .where(
            CryptoHistoricalData.asset_id == asset_id,
            CryptoHistoricalData.interval == interval
        )
        .order_by(CryptoHistoricalData.timestamp.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.post("/sync", response_model=List[CryptoAssetOut])
async def sync_crypto_assets(db: AsyncSession = Depends(get_session)):
    try:
        assets_data = await fetch_cmc_data_with_retry()
        stored_assets = []

        for asset_data in assets_data:
            quote = asset_data["quote"]["USD"]
            asset = CryptoAsset(
                id=asset_data["symbol"],
                cmc_rank=int(asset_data["cmc_rank"]),
                symbol=asset_data["symbol"],
                name=asset_data["name"],
                supply=float(asset_data["circulating_supply"]),
                max_supply=float(asset_data["max_supply"]) if asset_data["max_supply"] else None,
                market_cap=float(quote["market_cap"]),
                volume_24h=float(quote["volume_24h"]),
                price_usd=float(quote["price"]),
                percent_change_24h=float(quote["percent_change_24h"]),
                vwap_24hr=float(quote["vwap_24h"]) if quote["vwap_24h"] else None,
                explorer=asset_data.get("explorer")
            )

            existing = await db.execute(
                select(CryptoAsset).where(CryptoAsset.id == asset.id)
            )
            existing_asset = existing.scalar_one_or_none()

            if existing_asset:
                for key, value in asset.__dict__.items():
                    if not key.startswith("_"):
                        setattr(existing_asset, key, value)
            else:
                db.add(asset)

            stored_assets.append(asset)

        await db.commit()
        return stored_assets

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[CryptoAssetOut])
async def get_crypto_assets(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(CryptoAsset)
        .order_by(CryptoAsset.cmc_rank)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.get("/{asset_id}", response_model=CryptoAssetOut)
async def get_crypto_asset(asset_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(CryptoAsset).where(CryptoAsset.id == asset_id)
    )
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.post("/assets", response_model=CryptoAssetOut)
async def create_crypto_asset(asset: CryptoAssetCreate, db: AsyncSession = Depends(get_session)):
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
        tvl_ratio=asset.tvl_ratio
    )
    db.add(db_asset)
    await db.commit()
    await db.refresh(db_asset)
    return db_asset

@router.get("/assets", response_model=List[CryptoAssetOut])
async def get_crypto_assets(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CryptoAsset))
    return result.scalars().all()

@router.get("/assets/{asset_id}", response_model=CryptoAssetOut)
async def get_crypto_asset(asset_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CryptoAsset).where(CryptoAsset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset
