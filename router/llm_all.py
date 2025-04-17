from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from database import get_session
from models.llm_idea import LLMIdea
from models.llm_message import LLMMessage
from models.llm_snippet import LLMSnippet
from models.llm_memory_collection import LLMMemoryCollection
from models.llm_memory_snippet import LLMMemorySnippet

from schemas.llm_idea import LLMIdeaCreate, LLMIdeaOut
from schemas.llm_message import LLMMessageCreate, LLMMessageOut
from schemas.llm_snippet import LLMSnippetCreate, LLMSnippetOut
from schemas.llm_memory_collection import LLMMemoryCollectionCreate, LLMMemoryCollectionOut
from schemas.llm_memory_snippet import LLMMemorySnippetCreate, LLMMemorySnippetOut

router = APIRouter()

# === LLM Ideas ===
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

# === LLM Messages ===
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

# === LLM Snippets ===
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

# === Memory Collections ===
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

# === Attach Snippet to Collection ===
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
