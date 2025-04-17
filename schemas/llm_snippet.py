from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class LLMSnippetCreate(BaseModel):
    idea_id: Optional[UUID] = None
    title: Optional[str] = None
    content: str
    source: Optional[str] = "chat"

class LLMSnippetOut(BaseModel):
    id: UUID
    user_id: str
    idea_id: Optional[UUID]
    title: Optional[str]
    content: str
    source: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
