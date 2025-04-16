from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base
import uuid

class LLMKey(Base):
    __tablename__ = "llm_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    provider = Column(String, nullable=False)  # e.g. 'openai', 'anthropic'
    api_key = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
 