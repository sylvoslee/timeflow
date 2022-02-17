from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import validator
from datetime import datetime


class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    active: bool
    created_at: datetime
    updated_at: datetime
