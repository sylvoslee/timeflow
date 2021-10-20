from typing import Optional
from sqlmodel import Field, SQLModel, Field, create_engine

con_str = f"sqlite:///database.sqlite"
engine = create_engine(con_str, echo=True)


class Epic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    epic_name: str


class TimeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    epic_name: str
    start_time: str
    end_time: str

class User(SQLModel, table=True):
    id: Optional [int] = Field(default=None, primary_key=True)
    user_id: str
    user_name: str
    user_surname: str
    user_email: str

def create_db():
    SQLModel.metadata.create_all(engine)
