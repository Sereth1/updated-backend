from sqlalchemy import Column, String
from database import Base

class LLMProvider(Base):
    __tablename__ = "llm_providers"

    id = Column(String, primary_key=True)
    label = Column(String, nullable=False)
