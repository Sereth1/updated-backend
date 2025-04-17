from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from models.llm.llm_provider import LLMProvider
from schemas.llm.llm_provider import LLMProviderOut
from typing import List

router = APIRouter()

@router.get("/llm-providers", response_model=List[LLMProviderOut])
async def get_all_llm_providers(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMProvider))
    return result.scalars().all()
