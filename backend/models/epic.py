from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import validator
from datetime import datetime


class Epic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    work_area: str
    client_id: int = Field(foreign_key="client.id")
