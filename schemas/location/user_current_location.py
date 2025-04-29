from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCurrentLocation(BaseModel):
    user_id: str
    ip: str
    country: str
    city: str
    region: str
    timezone: Optional[str]
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
