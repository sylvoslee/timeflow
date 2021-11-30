from fastapi import *
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import OperationalError
from models import Epic, TimeLog, User, engine, create_db, Client
from utils import *
from fastapi.responses import HTMLResponse
import datetime
from dominate.tags import table, tr, td, style, div, thead, tbody, strong

# strftime("%m/%d/%Y, %H:%M:%S")

app = FastAPI()
session = Session(engine)


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


# For Developer Dashboard page (ddashboard)

# Get months numbers in a strings list
@app.get("/api/months")
async def get_months():
    months_list = []
    for i in range(1, 13):
        j = str(i)
        months_list.append(j)
    return months_list


# HTML testing table
@app.get("/html/table_test", response_class=HTMLResponse)
async def get_html():
    _table = table(border="1", style="border-collapse:collapse;border-spacing:2")
    _thead, _tbody = _table.add(thead(), tbody())
    _tr = _thead.add(tr())
    with _tr:
        td(strong("user id"))
        td("month")
        td("epic")
        td("days worked")
    _tr2 = _tbody.add(tr())
    with _tr2:
        td("user%id")
        td("%month")
        td("%epic")
        td("%days worked")

    return _table.render()


# Get work hours for Developer Dashboard (ddashboard)
@app.post(
    "/api/ddashboard/table/{user_initials},{month},{epic_name}",
    response_class=HTMLResponse,
)
async def post_ddashboard_work_days(
    user_initials: str,
    month: str,
    epic_name: str,
) -> str:

    # searching for work_days with selected arguments
    # print(2, epic_name)
    statement = (
        select(TimeLog.work_hours)
        .where(TimeLog.user_initials == user_initials)
        .where(TimeLog.month == month)
        .where(TimeLog.epic_name == epic_name)
    )
    work_hours_list = []
    results = session.exec(statement).all()
    for result in results:
        work_hours_list.append(result)
    work_days = "{:.2f}".format(sum(work_hours_list) / 8)
    work_days_str = str(work_days)

    # HTML table for ddashboard
    _table = table(
        border="1",
        style="overflow:hidden;padding:10px 5px;border-collapse:collapse;border-spacing:2;font-size:15px",
        cellpadding="10",
    )
    _thead, _tbody = _table.add(thead(), tbody())
    _tr = _thead.add(
        tr(
            style="border-color:inherit;text-align:center;vertical-align:top;background-color: #96D4D4"
        )
    )
    with _tr:
        td(strong("user id"))
        td(strong("month"))
        td(strong("epic"))
        td(strong("days worked"))
    _tr2 = _tbody.add(tr())
    with _tr2:
        td("%s" % user_initials)
        td("%s" % month)
        td("%s" % epic_name)
        td(work_days_str)
    return _table.render()


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
