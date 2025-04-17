from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class LLMMemorySnippetCreate(BaseModel):
    snippet_id: UUID

class LLMMemorySnippetOut(BaseModel):
    id: UUID
    collection_id: UUID
    snippet_id: UUID
    added_at: datetime

    class Config:
        orm_mode = True
