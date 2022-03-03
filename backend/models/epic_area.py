from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class EpicArea(SQLModel, table=True):
    """Creates an SQLModel for epic areas"""

    id: Optional[int] = Field(default=None, primary_key=True)
    epic_id: int = Field(foreign_key="epic.id")
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
