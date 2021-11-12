from fastapi import FastAPI
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import OperationalError
from models import Epic, TimeLog, User, engine, create_db
import datetime
# strftime("%m/%d/%Y, %H:%M:%S")

app = FastAPI()
session = Session(engine)

def string_to_datetime(date_string):
    date = datetime.datetime.strptime(
    date_string, "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    return date

def datetime_to_string(date_date):
    date_string = date_date.strftime("%m/%d/%Y, %H:%M:%S")
    return date_string

def get_user_worktime_by_epic(user_id, epic_name, search_start_time, search_end_time):
    statement = select(TimeLog).where(TimeLog.user_id == user_id).where(TimeLog.epic_name == epic_name).where(TimeLog.search_start_time == search_start_time)
    by_user = []
    for result in results:
        starting_time = string_to_datetime(result.start_time)
        ending_time = string_to_datetime(result.end_time)
        working_time = ending_time - starting_time
        by_user.append(working_time)
    l_sum = sum(by_user, datetime.timedelta())
    work_time_sum = str(l_sum)
    msg = f"""total work time spent by user {user_id} on epic {epic_name} is {work_time_sum}
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

#For dashboard page
    #Get timelogs
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
                , user_id is {result.user_id}
                , start date {start_time.strftime("%m/%d/%Y, %H:%M:%S")} 
                end date is {end_time.strftime("%m/%d/%Y, %H:%M:%S")}
                and work time is {str(work_time)}
                """
        d = result.dict()
        d["message"] = msg
        out.append(d)
    return out 

#For search page
    #Get TimeLog by epic_id
@app.get("/api/epics/{epic_id}") 
async def get_epic_id(epic_id):
        
    statement = select(TimeLog).where(TimeLog.epic_id == epic_id)
    results = session.exec(statement).all()
    by_epic = []
    for result in results:
        starting_time = string_to_datetime(result.start_time)
        ending_time = string_to_datetime(result.end_time)
        working_time = ending_time - starting_time
        by_epic.append(working_time)
    
    l_sum = sum(by_epic, datetime.timedelta()) # displays working_time spend by all on the same epic
    work_time_sum = str(l_sum)
    msg = f"""total work time on this epic is {work_time_sum}
           """
    return msg

#For Work Time page 
    #Get TimeLog by user_id and epic_name   
@app.get("/api/timelogs/{user_id},{epic_name}") 
async def get_user_by_epic_name(user_id, epic_name):
    get_user = get_user_worktime_by_epic(user_id, epic_name)
    return get_user

#Get full user_id list
@app.get("/api/users")
async def users():
    statement = select(User.user_id)
    results = session.exec(statement).all()
    return results

#Get full epic_name list
@app.get("/api/epics")
async def epics():
    statement = select(Epic.epic_name)
    results = session.exec(statement).all()
    return results

@app.post("/api/user/")
async def user(user: User):
    session.add(user)
    session.commit()

@app.post("/api/epic/")
async def epic(epic: Epic):
    session.add(epic)
    session.commit()

@app.post("/api/timelog/")
async def timelog(timelog: TimeLog):
    session.add(timelog)
    session.commit()
