# models/llm_memory_snippet.py
from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base
import uuid

class LLMMemorySnippet(Base):
    __tablename__ = "llm_memory_snippets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    collection_id = Column(UUID, ForeignKey("llm_memory_collections.id", ondelete="CASCADE"), nullable=False)
    snippet_id = Column(UUID, ForeignKey("llm_snippets.id", ondelete="CASCADE"), nullable=False)
    added_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("collection_id", "snippet_id", name="unique_snippet_per_collection"),
    )
