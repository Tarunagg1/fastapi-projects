from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime

class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    uid: uuid.UUID
    title: str
    author: str
    published: bool
    published_date: datetime
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

class BookCreateModel(BaseModel):
    title: str
    author: str
    published: bool
    published_date: datetime
    page_count: int
    language: str

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    published: bool | None = None
    published_date: datetime | None = None
    page_count: int | None = None
    language: str | None = None