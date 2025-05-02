from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID  # ✅ this!

# schemas/location/user_location_logs.py
class UserLocationLog(BaseModel):
    id: Optional[UUID] = None
    user_id: str
    ip: str
    country: str
    city: str
    region: str
    timezone: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

