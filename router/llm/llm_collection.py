from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from database import get_session
from models.llm.llm_memory_collection import LLMMemoryCollection
from models.llm.llm_memory_snippet import LLMMemorySnippet
from models.llm.llm_snippet import LLMSnippet
from schemas.llm.llm_memory_collection import LLMMemoryCollectionCreate, LLMMemoryCollectionOut
from schemas.llm.llm_memory_snippet import LLMMemorySnippetCreate, LLMMemorySnippetOut
from schemas.llm.llm_snippet import LLMSnippetOut

router = APIRouter()

@router.post("/llm-collections", response_model=LLMMemoryCollectionOut)
async def create_collection(user_id: str, payload: LLMMemoryCollectionCreate, db: AsyncSession = Depends(get_session)):
    collection = LLMMemoryCollection(user_id=user_id, **payload.dict())
    db.add(collection)
    await db.commit()
    await db.refresh(collection)
    return collection

@router.get("/llm-collections/{user_id}", response_model=list[LLMMemoryCollectionOut])
async def get_user_collections(user_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMMemoryCollection).where(LLMMemoryCollection.user_id == user_id))
    return result.scalars().all()

@router.delete("/llm-collections/{collection_id}")
async def delete_collection(collection_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMMemoryCollection).where(LLMMemoryCollection.id == collection_id))
    collection = result.scalar_one_or_none()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    await db.delete(collection)
    await db.commit()
    return {"message": "Collection deleted"}

@router.put("/llm-collections/{collection_id}", response_model=LLMMemoryCollectionOut)
async def update_collection(collection_id: UUID, payload: LLMMemoryCollectionCreate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(LLMMemoryCollection).where(LLMMemoryCollection.id == collection_id))
    collection = result.scalar_one_or_none()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(collection, field, value)
    await db.commit()
    await db.refresh(collection)
    return collection

@router.post("/llm-collections/{collection_id}/add-snippet", response_model=LLMMemorySnippetOut)
async def add_snippet_to_collection(collection_id: UUID, payload: LLMMemorySnippetCreate, db: AsyncSession = Depends(get_session)):
    # Check for duplicates
    exists = await db.execute(
        select(LLMMemorySnippet).where(
            LLMMemorySnippet.collection_id == collection_id,
            LLMMemorySnippet.snippet_id == payload.snippet_id
        )
    )
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Snippet already in collection")

    link = LLMMemorySnippet(collection_id=collection_id, snippet_id=payload.snippet_id)
    db.add(link)
    await db.commit()
    await db.refresh(link)
    return link

@router.get("/llm-collections/{collection_id}/snippets", response_model=list[LLMSnippetOut])
async def get_snippets_in_collection(collection_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(LLMSnippet)
        .join(LLMMemorySnippet, LLMMemorySnippet.snippet_id == LLMSnippet.id)
        .where(LLMMemorySnippet.collection_id == collection_id)
    )
    return result.scalars().all()

@router.delete("/llm-collections/{collection_id}/snippets/{snippet_id}")
async def remove_snippet_from_collection(collection_id: UUID, snippet_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(LLMMemorySnippet)
        .where(
            LLMMemorySnippet.collection_id == collection_id,
            LLMMemorySnippet.snippet_id == snippet_id
        )
    )
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Snippet not linked to this collection")

    await db.delete(link)
    await db.commit()
    return {"message": "Snippet removed from collection"} 