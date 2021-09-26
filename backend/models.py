from typing import Optional
from sqlmodel import Field, SQLModel, Field, create_engine

sqlite_file_name = "database_.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


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


if __name__ == "__main__":
    # create_db()
    pass
