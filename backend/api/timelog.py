from fastapi import APIRouter
from models import TimeLog, User, engine
from sqlmodel import Session, select, SQLModel
from utils import *

router = APIRouter()
session = Session(engine)


# Post timelog
@router.post("/api/timelogs/create")
async def timelog(timelog: TimeLog):
    statement = select(User.user_surname).where(
        User.user_initials == timelog.user_initials
    )
    surname = session.exec(statement).first()

    startt_to_dt = string_to_datetime(timelog.start_time)
    # Timelog.month
    month_from_dt = startt_to_dt.month
    # Timelog.year
    year_from_dt = startt_to_dt.year
    # Timelog.work_hours
    work_delta = string_to_datetime(timelog.end_time) - string_to_datetime(
        timelog.start_time
    )
    work_delta_hours = work_delta.seconds / 3600
    work_hours = "{:.2f}".format(work_delta_hours)

    new_timelog = TimeLog(
        id=timelog.id,
        user_initials=timelog.user_initials,
        start_time=timelog.start_time,
        end_time=timelog.end_time,
        client_name=timelog.client_name,
        epic_name=timelog.epic_name,
        work_hours=work_hours,
        month=month_from_dt,
        year=year_from_dt,
    )

    session.add(new_timelog)
    session.commit()


# Get timelogs
@router.get("/api/timelogs/read")
async def get_timelogs():
    statement = select(TimeLog)
    results = session.exec(statement).all()
    out = []
    for result in results:
        start_time = datetime.datetime.strptime(
            # 2021-09-26T17:25:00.000Z
            result.start_time,
            "%Y-%m-%dT%H:%M:%S.%fz",
        )
        end_time = datetime.datetime.strptime(
            # 2021-09-26T17:25:00.000Z
            result.end_time,
            "%Y-%m-%dT%H:%M:%S.%fz",
        )
        work_time = end_time - start_time
        msg = f"""epic_name is {result.epic_name}
                , user_id is {result.user_initials}
                , start date {start_time.strftime("%m/%d/%Y, %H:%M:%S")} 
                end date is {end_time.strftime("%m/%d/%Y, %H:%M:%S")}
                and work time is {str(work_time)}
                """
        d = result.dict()
        d["message"] = msg
        out.append(d)
    return out
