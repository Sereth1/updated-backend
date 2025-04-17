# models/llm_idea.py
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base
import uuid

class LLMIdea(Base):
    __tablename__ = "llm_ideas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    title = Column(String, nullable=True)
    llm_key_id = Column(UUID, ForeignKey("llm_keys.id"), nullable=True)  # optional
    created_at = Column(DateTime, server_default=func.now())
