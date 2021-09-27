from typing import Optional
from sqlmodel import Field, SQLModel, Field, create_engine

con_str = f"sqlite:///database.sqlite"
engine = create_engine(con_str, echo=True)


class Epic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    label: str
    value: int
    disabled: bool = False


class TimeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    epic_id: int
    start_time: str
    end_time: str


def create_db():
    SQLModel.metadata.create_all(engine)
