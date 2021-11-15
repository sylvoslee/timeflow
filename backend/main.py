from fastapi import FastAPI
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import OperationalError
from models import Epic, TimeLog, User, engine, create_db, Client
from utils import string_to_datetime
import datetime

# strftime("%m/%d/%Y, %H:%M:%S")

app = FastAPI()
session = Session(engine)


def string_to_datetime_GMT(date_string):
    date = datetime.datetime.strptime(date_string, "%a %b %d %Y %H:%M:%S %Z%z")
    return date


def string_to_datetime_work(date_string):
    date = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date


def datetime_to_string(date_date):
    date_string = date_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return date_string


def time_period(time_of_start, time_of_end):
    starting_time = string_to_datetime_work(time_of_start)
    ending_time = string_to_datetime_work(time_of_end)
    working_time = ending_time - starting_time
    return working_time


def get_user_worktime_random(user_initials, epic_name, start_time, end_time):
    start_time_cut = start_time[:33]
    end_time_cut = end_time[:33]
    start_time_dt = string_to_datetime_GMT(start_time_cut)
    start_time_st = datetime_to_string(start_time_dt)
    end_time_dt = string_to_datetime_GMT(end_time_cut)
    end_time_st = datetime_to_string(end_time_dt)
    statement = (
        select(TimeLog)
        .where(TimeLog.user_initials == user_initials)
        .where(TimeLog.epic_name == epic_name)
        .where(TimeLog.start_time < end_time_st, TimeLog.end_time > start_time_st)
    )
    results = session.exec(statement).all()
    work_list = []
    for result in results:
        if result.start_time > start_time_st and result.end_time < end_time_st:
            working_time = time_period(result.start_time, result.end_time)
        elif result.start_time > start_time_st and result.end_time >= end_time_st:
            working_time = time_period(result.start_time, end_time_st)
        elif result.start_time <= start_time_st and result.end_time < end_time_st:
            working_time = time_period(start_time_st, result.end_time)
        else:
            working_time = time_period(start_time_st, end_time_st)
        work_list.append(working_time)
    l_sum = sum(work_list, datetime.timedelta())
    work_time_sum = str(l_sum)
    msg = f"""total work time spent by user {user_initials} from {start_time_cut} to {end_time} on epic {epic_name} is {work_time_sum}
            """
    return msg


@app.on_event("startup")
def on_startup():
    try:
        statement = select(TimeLog)
        results = session.exec(statement)
    except OperationalError:
        create_db()


@app.get("/hello/{name}")
async def hello_name(name):
    return {"message": f"Hello {name}"}


# For dashboard page
# Get timelogs
@app.get("/api/timelogs")
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


# For Work Time page
# Get TimeLog by user_id, epic_name and time period
@app.get("/api/timelogs/{user_id},{epic_name},{start_time},{end_time}")
async def get_user_by_epic_name(user_id, epic_name, start_time, end_time):
    get_user = get_user_worktime_random(user_id, epic_name, start_time, end_time)
    return get_user


# Get full user_id list
@app.get("/api/users")
async def users():
    statement = select(User.user_initials)
    results = session.exec(statement).all()
    return results


# Get full client list
@app.get("/api/clients")
async def clients():
    statement = select(Client.client_name)
    results = session.exec(statement).all()
    return results


# Get full epic_name list
@app.get("/api/epics")
async def epics():
    statement = select(Epic.epic_name)
    results = session.exec(statement).all()
    return results


# Post user
@app.post("/api/user/")
async def user(user: User):
    session.add(user)
    session.commit()


# Post client
@app.post("/api/client/")
async def client(client: Client):
    session.add(client)
    session.commit()


# Post epic
@app.post("/api/epic/")
async def epic(epic: Epic):
    session.add(epic)
    session.commit()


# Post timelog
@app.post("/api/timelog/")
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
