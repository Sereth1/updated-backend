# models/llm_snippet.py
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base
import uuid

class LLMSnippet(Base):
    __tablename__ = "llm_snippets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    idea_id = Column(UUID, ForeignKey("llm_ideas.id"), nullable=True)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    source = Column(String, nullable=True, default="chat")  # or 'manual'
    created_at = Column(DateTime, server_default=func.now())
