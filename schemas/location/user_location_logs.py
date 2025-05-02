from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

# Response model
class UserLocationLog(BaseModel):
    id: UUID
    user_id: str
    ip: str
    country: str
    city: str
    region: str
    timezone: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

# Create model
class UserLocationLogCreate(BaseModel):
    user_id: str
    ip: str
    country: str
    city: str
    region: str
    timezone: Optional[str]
