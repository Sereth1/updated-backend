from pydantic import BaseModel

class LLMProviderOut(BaseModel):
    id: str
    label: str

    class Config:
        orm_mode = True
