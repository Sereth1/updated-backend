from sqlalchemy import Column, String, Boolean, DateTime
from database import Base

class User(Base):
    __tablename__ = "user"  # ✅ this matches your Neon table name exactly

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    emailVerified = Column(Boolean)
    image = Column(String)
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)
