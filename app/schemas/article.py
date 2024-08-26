from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ArticleBase(BaseModel):
    title: str = Field(..., max_length=512)
    content: str
    author_name: Optional[str] = Field(..., max_length=100)
    meta_description: Optional[str] = Field(None, max_length=160)

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleInDBBase(ArticleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ArticlePublic(ArticleInDBBase):
    pass
