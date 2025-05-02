from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from database import get_session
from models.location.user_location_logs import UserLocationLog as DBUserLocationLog
from schemas.location.user_location_logs import UserLocationLog as UserLocationLogSchema
from schemas.location.user_location_logs import UserLocationLogCreate
from typing import List
from datetime import datetime
import uuid

router = APIRouter()

@router.get("/user-location-logs", response_model=List[UserLocationLogSchema])
async def get_user_location_logs(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(DBUserLocationLog))
    return result.scalars().all()

@router.get("/user-location-logs/{user_location_log_id}", response_model=UserLocationLogSchema)
async def get_user_location_log(user_location_log_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(DBUserLocationLog).where(DBUserLocationLog.id == uuid.UUID(user_location_log_id))
    )
    user_location_log = result.scalar_one_or_none()
    if not user_location_log:
        raise HTTPException(status_code=404, detail="User location log not found")
    return user_location_log

@router.get("/user-location-logs/last/{user_id}", response_model=UserLocationLogSchema)
async def get_last_user_location_log(user_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(DBUserLocationLog)
        .where(DBUserLocationLog.user_id == user_id)
        .order_by(DBUserLocationLog.created_at.desc())
        .limit(1)
    )
    last_log = result.scalar_one_or_none()
    if not last_log:
        raise HTTPException(status_code=404, detail="No location logs found for this user")
    return last_log

@router.post("/user-location-logs", response_model=UserLocationLogSchema)
async def create_user_location_log(user_location_log: UserLocationLogCreate, db: AsyncSession = Depends(get_session)):
    try:
        new_log = DBUserLocationLog(
            user_id=user_location_log.user_id,
            ip=user_location_log.ip,
            country=user_location_log.country,
            city=user_location_log.city,
            region=user_location_log.region,
            timezone=user_location_log.timezone,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_log)
        await db.commit()
        await db.refresh(new_log)
        return new_log
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/user-location-logs/{user_location_log_id}", response_model=UserLocationLogSchema)
async def update_user_location_log(user_location_log_id: str, user_location_log: UserLocationLogSchema, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(DBUserLocationLog).where(DBUserLocationLog.id == uuid.UUID(user_location_log_id))
    )
    existing_log = result.scalar_one_or_none()
    if not existing_log:
        raise HTTPException(status_code=404, detail="User location log not found")

    for field in ["ip", "country", "city", "region", "timezone"]:
        setattr(existing_log, field, getattr(user_location_log, field))
    existing_log.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(existing_log)
    return existing_log
