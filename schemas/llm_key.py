from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LLMKeyCreate(BaseModel):
    provider: str
    api_key: str

class LLMKeyOut(BaseModel):
    id: str
    provider: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
