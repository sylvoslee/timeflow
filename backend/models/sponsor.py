from typing import Optional
from sqlmodel import Field, SQLMOdel
from datetime import datetime


class Sponsor(SQLModel, table=True):
    """Create an SQLModel for sponsors"""

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    name: str
    short_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
