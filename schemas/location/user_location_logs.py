from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID  # ✅ this!

# schemas/location/user_location_logs.py
from pydantic import BaseModel
from typing import Optional

class UserLocationLogCreate(BaseModel):
    user_id: str
    ip: str
    country: str
    city: str
    region: str
    timezone: Optional[str]


    model_config = {
        "from_attributes": True
    }

