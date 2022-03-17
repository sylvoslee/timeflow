from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import validator
from datetime import datetime, date


class Rate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    client_id: int = Field(foreign_key="client.id")
    valid_from: date
    valid_to: date
    amount: float  # currency: EUR
    created_at: datetime
    updated_at: datetime
    is_active: bool
