from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from database import get_session
from models.llm.llm_snippet import LLMSnippet
from schemas.llm.llm_snippet import LLMSnippetCreate, LLMSnippetOut

router = APIRouter()

@router.post("/llm-snippets", response_model=LLMSnippetOut)
async def create_snippet(user_id: str, payload: LLMSnippetCreate, db: AsyncSession = Depends(get_session)):
    snippet = LLMSnippet(user_id=user_id, **payload.dict())
    db.add(snippet)
    await db.commit()
    await db.refresh(snippet)
    return snippet

@router.get("/llm-snippets/{user_id}", response_model=list[LLMSnippetOut])
async def get_user_snippets(user_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMSnippet).where(LLMSnippet.user_id == user_id))
    return result.scalars().all()

@router.delete("/llm-snippets/{snippet_id}")
async def delete_snippet(snippet_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMSnippet).where(LLMSnippet.id == snippet_id))
    snippet = result.scalar_one_or_none()
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    await db.delete(snippet)
    await db.commit()
    return {"message": "Snippet deleted"}

@router.put("/llm-snippets/{snippet_id}", response_model=LLMSnippetOut)
async def update_snippet(snippet_id: UUID, payload: LLMSnippetCreate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMSnippet).where(LLMSnippet.id == snippet_id))
    snippet = result.scalar_one_or_none()
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(snippet, field, value)
    await db.commit()
    await db.refresh(snippet)
    return snippet 