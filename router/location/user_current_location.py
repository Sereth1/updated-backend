from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.future import select
from database import get_session
from models.location.user_current_location import UserCurrentLocation as DBCurrentLocation
from schemas.location.user_current_location import UserCurrentLocation
from datetime import datetime

router = APIRouter()

@router.post("/user-current-location", response_model=UserCurrentLocation)
async def upsert_user_current_location(
    data: UserCurrentLocation,
    db: AsyncSession = Depends(get_session)
):
    stmt = pg_insert(DBCurrentLocation).values(
        user_id=data.user_id,
        ip=data.ip,
        country=data.country,
        city=data.city,
        region=data.region,
        timezone=data.timezone,
        updated_at=datetime.utcnow()
    ).on_conflict_do_update(
        index_elements=['user_id'],
        set_={
            "ip": data.ip,
            "country": data.country,
            "city": data.city,
            "region": data.region,
            "timezone": data.timezone,
            "updated_at": datetime.utcnow()
        }
    )

    await db.execute(stmt)
    await db.commit()

    result = await db.get(DBCurrentLocation, data.user_id)
    return result


@router.get("/user-current-location/{user_id}", response_model=UserCurrentLocation)
async def get_user_current_location(user_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(DBCurrentLocation).where(DBCurrentLocation.user_id == user_id)
    )
    current_location = result.scalar_one_or_none()
    
    if not current_location:
        raise HTTPException(status_code=404, detail="Current location not found for this user")
    
    return current_location
