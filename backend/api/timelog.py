from fastapi import APIRouter
from ..utils import engine, string_to_datetime
from sqlmodel import Session, select, SQLModel, or_
from ..utils import engine
from ..models.user import User
from ..models.timelog import TimeLog

router = APIRouter(prefix="/api/timelogs", tags=["timelog"])

session = Session(engine)


# Post timelog
# example: timelog.start_time = "2022-01-19T08:30:00.000Z"
@router.post("/")
async def timelog(timelog: TimeLog):
    statement1 = (
        select(TimeLog)
        .where(TimeLog.user_id == timelog.user_id)
        .where(TimeLog.start_time >= timelog.start_time)
        .where(TimeLog.start_time <= timelog.end_time)
    )
    statement2 = (
        select(TimeLog)
        .where(TimeLog.user_id == timelog.user_id)
        .where(TimeLog.end_time >= timelog.start_time)
        .where(TimeLog.end_time <= timelog.end_time)
    )
    results1 = session.exec(statement1).all()
    results2 = session.exec(statement2).all()
    if results1 or results2:
        return "currently posted timelog overlaps with another timelog"
    else:
        session.add(timelog)
        session.commit()
        session.refresh(timelog)
        return timelog


# Get all timelogs
@router.get("/")
async def get_timelogs_all():
    statement = select(TimeLog)
    results = session.exec(statement).all()
    return results


# Get list of timelogs by user_id
@router.get("/users/{user_id}")
async def get_timelog_user_id(user_id: str):
    statement = select(TimeLog).where(TimeLog.user_id == user_id)
    results = session.exec(statement).all()
    return results


# Get list of timelogs
@router.get("/lists/{username},{epic_name},{month}")
async def get_timelog_list(
    username: str = None, epic_name: str = None, month: int = None
):
    if username != None:
        if epic_name != None:
            if month != None:
                statement = (
                    select(TimeLog)
                    .where(TimeLog.username == username)
                    .where(TimeLog.epic_name == epic_name)
                    .where(TimeLog.month == month)
                )
            else:
                statement = (
                    select(TimeLog)
                    .where(TimeLog.username == username)
                    .where(TimeLog.epic_name == epic_name)
                )
        else:
            statement = (
                select(TimeLog)
                .where(TimeLog.username == username)
                .where(TimeLog.month == month)
            )
    else:
        statement = (
            select(TimeLog)
            .where(TimeLog.epic_name == epic_name)
            .where(TimeLog.month == month)
        )
    results = session.exec(statement).all()
    return results


# Update timelogs
@router.put("/")
async def update_timelogs(
    username: str = None,
    epic_name: str = None,
    date: str = None,
    start_time: str = None,
):
    date_dt = string_to_datetime(date)
    date_string = date_dt.date

    statement = (
        select(TimeLog)
        .where(TimeLog.username == username)
        .where(TimeLog.epic_name == epic_name)
    )
    timelog_to_update = session.exec(statement).one()
    timelog_to_update.start_time = start_time
    session.add(timelog_to_update)
    session.commit()
    session.refresh(timelog_to_update)
    return True


# Delete timelogs
@router.delete("/")
async def delete_timelogs(
    timelog_id: str = None,
):
    statement = select(TimeLog).where(TimeLog.id == timelog_id)
    result = session.exec(statement).one()
    timelogs_to_delete = result
    session.delete(timelogs_to_delete)
    session.commit()
    return True
