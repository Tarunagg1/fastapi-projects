# from pydantic import BaseModel, Field
from typing import Optional, List
from sqlmodel import SQLModel, Field

class EventModel(SQLModel, table=True):
    id: int
    page: Optional[str] = ""
    description: Optional[str] = ""

class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="My description")


class EventUpdateSchema(SQLModel):
    description: str


class EventListSchema(SQLModel):
    results: list[EventModel]
    count: int