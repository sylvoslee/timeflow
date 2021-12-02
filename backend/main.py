from fastapi import *
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import OperationalError
from models import Epic, TimeLog, User, engine, create_db, Client
from utils import *
from fastapi.responses import HTMLResponse
import datetime
from dominate.tags import table, tr, td, style, div, thead, tbody, strong
from api import user, timelog

# strftime("%m/%d/%Y, %H:%M:%S")

app = FastAPI()
session = Session(engine)
app.include_router(user.router)
app.include_router(timelog.router)


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
