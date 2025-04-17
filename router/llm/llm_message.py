from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from database import get_session
from models.llm.llm_message import LLMMessage
from schemas.llm.llm_message import LLMMessageCreate, LLMMessageOut

router = APIRouter()

@router.post("/llm-messages", response_model=LLMMessageOut)
async def create_message(payload: LLMMessageCreate, db: AsyncSession = Depends(get_session)):
    msg = LLMMessage(**payload.dict())
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

@router.get("/llm-messages/{idea_id}", response_model=list[LLMMessageOut])
async def get_messages_for_idea(idea_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMMessage).where(LLMMessage.idea_id == idea_id))
    return result.scalars().all() 