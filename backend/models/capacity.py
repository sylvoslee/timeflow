from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class Capacity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    team_id: int = Field(foreign_key="team.id")
    year: int
    month: int
    days: int
    created_at: datetime
    updated_at: datetime
    is_locked: bool = False
