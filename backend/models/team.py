from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class Team(SQLModel, table=True):
    """Create an SQLModel for teams"""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    short_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
