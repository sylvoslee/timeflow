from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import validator
from datetime import datetime, date


class Epic(SQLModel, table=True):
    """Create an SQLModel for epic entity"""

    id: Optional[int] = Field(default=None, primary_key=True)
    short_name: str
    name: str
    team_id: int
    sponsor_id: int = Field(foreign_key="sponsor.id")
    start_date: date
    is_active: bool
    created_at: datetime
    updated_at: datetime
