from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import validator
from datetime import datetime


class EpicArea(SQLModel, table=True):
    """
    Creates an SQLModel for epic areas
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    epic_id: int = Field(foreign_key="epic.id")
    name: str
    active: bool
    created_at: datetime
    updated_at: datetime
