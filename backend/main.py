from fastapi import FastAPI
from sqlmodel import Session, select
from models import Epic, TimeLog, engine
import datetime

# strftime("%m/%d/%Y, %H:%M:%S")

app = FastAPI()
session = Session(engine)

# example of url value to python function value
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
        msg = f"""epic_id is {result.epic_id}
                , start date {start_time.strftime("%m/%d/%Y, %H:%M:%S")} 
                and end date {result.end_time}
                """
        d = result.dict()
        d["message"] = msg
        out.append(d)
    return out


@app.post("/api/timelog/")
async def timelog(timelog: TimeLog):
    session.add(timelog)
