from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from database import get_session
from models.llm.llm_idea import LLMIdea
from schemas.llm.llm_idea import LLMIdeaCreate, LLMIdeaOut

router = APIRouter()

@router.post("/llm-ideas", response_model=LLMIdeaOut)
async def create_idea(user_id: str, payload: LLMIdeaCreate, db: AsyncSession = Depends(get_session)):
    idea = LLMIdea(user_id=user_id, **payload.dict())
    db.add(idea)
    await db.commit()
    await db.refresh(idea)
    return idea

@router.get("/llm-ideas/{user_id}", response_model=list[LLMIdeaOut])
async def get_user_ideas(user_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMIdea).where(LLMIdea.user_id == user_id))
    return result.scalars().all()

@router.delete("/llm-ideas/{idea_id}")
async def delete_idea(idea_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMIdea).where(LLMIdea.id == idea_id))
    idea = result.scalar_one_or_none()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    await db.delete(idea)
    await db.commit()
    return {"message": "Idea deleted"}

@router.put("/llm-ideas/{idea_id}", response_model=LLMIdeaOut)
async def update_idea(idea_id: UUID, payload: LLMIdeaCreate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMIdea).where(LLMIdea.id == idea_id))
    idea = result.scalar_one_or_none()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(idea, field, value)
    await db.commit()
    await db.refresh(idea)
    return idea 