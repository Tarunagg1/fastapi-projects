from click import DateTime
from pydantic import BaseModel, EmailStr, Field
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING


class UserInDb(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
    email: EmailStr = Field(index=True, unique=True, nullable=False)
    password: str | None = Field(nullable=False, default=None)
    google_id: str | None = Field(default=None, nullable=True, index=True, unique=True)
    auth_provider: str | None = Field(default="email")
    reset_token: str | None  = Field(default=None, nullable=True)
    reset_token_expires: datetime | None = Field(
        sa_column=Column(DateTime, nullable=True)
    )
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)