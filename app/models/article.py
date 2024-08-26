from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Article(SQLModel, table=True):
    __tablename__ = "articles"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(..., max_length=512, unique=True)
    content: str
    author_name: Optional[str] = Field(None, max_length=100)
    meta_description: Optional[str] = Field(None, max_length=160)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)
    
    def __repr__(self):
        return f"<Article(title={self.title})>"
