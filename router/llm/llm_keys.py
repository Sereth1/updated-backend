from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from models.llm.llm_key import LLMKey
from schemas.llm.llm_key import LLMKeyCreate, LLMKeyOut
from typing import List
import uuid

router = APIRouter()

@router.post("/llm-keys", response_model=LLMKeyOut, status_code=201)
async def create_llm_key(
    user_id: str,
    payload: LLMKeyCreate,
    db: AsyncSession = Depends(get_session)
):
    # Check if already exists
    existing = await db.execute(
        select(LLMKey).where(
            LLMKey.user_id == user_id,
            LLMKey.provider_id == payload.provider
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="API key for this provider already exists for this user."
        )

    new_key = LLMKey(
        user_id=user_id,
        provider_id=payload.provider,
        api_key=payload.api_key
    )
    db.add(new_key)
    await db.commit()
    await db.refresh(new_key)
    return new_key


@router.delete("/llm-keys/{id}", status_code=204)
async def delete_llm_key(id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMKey).where(LLMKey.id == id))
    key = result.scalar_one_or_none()
    if not key:
        raise HTTPException(status_code=404, detail="LLM key not found")
    await db.delete(key)
    await db.commit()

@router.put("/llm-keys/{id}", response_model=LLMKeyOut)
async def update_llm_key(
    id: str,
    payload: LLMKeyCreate,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(LLMKey).where(LLMKey.id == id))
    key = result.scalar_one_or_none()
    if not key:
        raise HTTPException(status_code=404, detail="LLM key not found")

    key.api_key = payload.api_key
    await db.commit()
    await db.refresh(key)
    return key


@router.get("/llm-keys/{user_id}", response_model=List[LLMKeyOut])
async def get_llm_keys(user_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMKey).where(LLMKey.user_id == user_id))
    return result.scalars().all()
