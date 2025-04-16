from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from models.user import User

router = APIRouter()

@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [user.__dict__ for user in users]  # 👈 works but includes internal SQLAlchemy stuff
