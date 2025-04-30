from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID  # ✅ this!

class UserLocationLog(BaseModel):
    id: UUID  # ✅ Fix here
    user_id: str
    ip: str
    country: str
    city: str
    region: str
    timezone: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }
