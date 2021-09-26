from fastapi import FastAPI
from models import Epic

app = FastAPI()

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
