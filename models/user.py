from sqlalchemy import Column, String, Boolean, DateTime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # UUID
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    emailVerified = Column(Boolean, default=False)
    image = Column(String)
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)
