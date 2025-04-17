from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class LLMIdeaCreate(BaseModel):
    title: Optional[str] = None
    llm_key_id: Optional[UUID] = None

class LLMIdeaOut(BaseModel):
    id: UUID
    user_id: str
    title: Optional[str]
    llm_key_id: Optional[UUID]
    created_at: datetime

    class Config:
        orm_mode = True
