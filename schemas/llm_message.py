from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class LLMMessageCreate(BaseModel):
    idea_id: UUID
    role: str  # 'user' or 'assistant'
    content: str

class LLMMessageOut(BaseModel):
    id: UUID
    idea_id: UUID
    role: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
