from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    emailVerified: bool
    image: Optional[str]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

    class Config:
        orm_mode = True  # ✅ needed to return SQLAlchemy models as JSON
