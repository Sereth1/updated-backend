from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from models.location.user_location_logs import UserLocationLog as DBUserLocationLog
from schemas.location.user_location_logs import UserLocationLog as UserLocationLogSchema
from typing import List
from datetime import datetime
import uuid

router = APIRouter()

# GET all logs
@router.get("/user_location-logs", response_model=List[UserLocationLogSchema])
async def get_user_location_logs(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(DBUserLocationLog))
    return result.scalars().all()


# GET single log by ID
@router.get("/user_location-logs/{user_location_log_id}", response_model=UserLocationLogSchema)
async def get_user_location_log(user_location_log_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(DBUserLocationLog).where(DBUserLocationLog.id == user_location_log_id)
    )
    user_location_log = result.scalar_one_or_none()
    if not user_location_log:
        raise HTTPException(status_code=404, detail="User location log not found")
    return user_location_log


# POST create new log
@router.post("/user_location-logs", response_model=UserLocationLogSchema)
async def create_user_location_log(user_location_log: UserLocationLogSchema, db: AsyncSession = Depends(get_session)):
    new_log = DBUserLocationLog(
        id=str(uuid.uuid4()),  # ✅ Generate UUID manually
        user_id=user_location_log.user_id,
        ip=user_location_log.ip,
        country=user_location_log.country,
        city=user_location_log.city,
        region=user_location_log.region,
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow(),
    )
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log


# PUT update existing log
@router.put("/user_location-logs/{user_location_log_id}", response_model=UserLocationLogSchema)
async def update_user_location_log(user_location_log_id: str, user_location_log: UserLocationLogSchema, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(DBUserLocationLog).where(DBUserLocationLog.id == user_location_log_id)
    )
    existing_log = result.scalar_one_or_none()
    if not existing_log:
        raise HTTPException(status_code=404, detail="User location log not found")

    # Update fields
    for field in ["ip", "country", "city", "region", "user_id"]:
        setattr(existing_log, field, getattr(user_location_log, field))
    existing_log.updatedAt = datetime.utcnow()

    await db.commit()
    await db.refresh(existing_log)
    return existing_log
