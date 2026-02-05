from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str
    name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class User(UserBase, table=True):
    id: Optional[str] = Field(primary_key=True, max_length=36)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime
    updated_at: datetime
    password_hash: str  # In a real app, store hashed password


class UserCreate(UserBase):
    password: str
    email: str


class UserRead(UserBase):
    id: str