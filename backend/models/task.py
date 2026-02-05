# from sqlmodel import SQLModel, Field, create_engine
# from typing import Optional
# from datetime import datetime, timezone

# class TaskBase(SQLModel):
#     title: str = Field(min_length=1, max_length=200)
#     description: Optional[str] = Field(default=None, max_length=1000)
#     completed: bool = Field(default=False)

# class Task(TaskBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: str = Field(index=True)  # User ID from JWT
#     created_at: datetime
#     updated_at: datetime

# class TaskUpdate(SQLModel):
#     title: Optional[str] = Field(default=None, min_length=1, max_length=200)
#     description: Optional[str] = Field(default=None, max_length=1000)

# class TaskCreate(TaskBase):
#     pass

# class TaskRead(TaskBase):
#     id: int
#     user_id: str
#     created_at: datetime
#     updated_at: datetime
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)

    # Set defaults at the database level using SQLModel syntax with timezone-aware datetimes
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime, nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime, nullable=False)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskRead(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
