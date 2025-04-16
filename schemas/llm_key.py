from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class LLMKeyCreate(BaseModel):
    provider: str  # this is the provider_id
    api_key: str

class LLMKeyOut(BaseModel):
    id: UUID
    user_id: str
    provider_id: str  # ✅ MATCHES MODEL
    api_key: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
