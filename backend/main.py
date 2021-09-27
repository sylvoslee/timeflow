from fastapi import FastAPI
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import OperationalError
from models import Epic, TimeLog, engine, create_db
import datetime

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


@app.get("/api/epics")
async def epics():
    epic1 = Epic(label="HyperlocalSOUTH", value=1)
    epic2 = Epic(label="HyperlocalNW", value=2)
    epic3 = Epic(label="MarketingKPIs", value=3)
    return [epic1, epic2, epic3]


@app.get("/api/timelogs")
async def get_timelogs():
    statement = select(TimeLog)
    results = session.exec(statement).all()
    out = []
    print(results)
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
        msg = f"""epic_id is {result.epic_id}
                , start date {start_time.strftime("%m/%d/%Y, %H:%M:%S")} 
                and end date {end_time.strftime("%m/%d/%Y, %H:%M:%S")}
                """
        d = result.dict()
        d["message"] = msg
        out.append(d)
    return out


@app.post("/api/timelog/")
async def timelog(timelog: TimeLog):
    session.add(timelog)
    session.commit()
