from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel, Field
from pydantic import validator
from datetime import datetime, date


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    short_name: str
    first_name: str
    last_name: str
    email: str
    role_id: int
    team_id: Optional[int] = None
    start_date: date
    created_at: datetime
    updated_at: datetime
    is_active: bool
