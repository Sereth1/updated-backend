from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from models.llm_key import LLMKey
from schemas.llm_key import LLMKeyCreate, LLMKeyOut
from typing import List
import uuid

router = APIRouter()

@router.post("/llm-keys", response_model=LLMKeyOut)
async def create_llm_key(
    user_id: str,
    payload: LLMKeyCreate,
    db: AsyncSession = Depends(get_session)
):
    new_key = LLMKey(
        user_id=user_id,
        provider=payload.provider,
        api_key=payload.api_key
    )
    db.add(new_key)
    await db.commit()
    await db.refresh(new_key)
    return new_key

@router.get("/llm-keys/{user_id}", response_model=List[LLMKeyOut])
async def get_llm_keys(user_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMKey).where(LLMKey.user_id == user_id))
    return result.scalars().all()
