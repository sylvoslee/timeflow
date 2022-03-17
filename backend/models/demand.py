from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class Demand(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="team.id")
    epic_id: int = Field(foreign_key="epic.id")
    year: int
    month: int
    days: int
    created_at: datetime
    updated_at: datetime
    is_locked: bool = False
