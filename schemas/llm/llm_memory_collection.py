from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class LLMMemoryCollectionCreate(BaseModel):
    title: str
    description: Optional[str] = None

class LLMMemoryCollectionOut(BaseModel):
    id: UUID
    user_id: str
    title: str
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
