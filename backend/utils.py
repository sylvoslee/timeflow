import datetime
from sqlmodel import Session, select, SQLModel, create_engine
from backend.models.user import User
from backend.models.timelog import TimeLog


con_str = f"sqlite:///backend/database.sqlite"
engine = create_engine(con_str, echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)


session = Session(engine)


def string_to_datetime(date_string):
    date = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date


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


def get_user_worktime(username, epic_name, start_time, end_time):
    start_time_cut = start_time[:33]
    end_time_cut = end_time[:33]
    start_time_dt = string_to_datetime_GMT(start_time_cut)
    start_time_st = datetime_to_string(start_time_dt)
    end_time_dt = string_to_datetime_GMT(end_time_cut)
    end_time_st = datetime_to_string(end_time_dt)
    statement = (
        select(TimeLog)
        .where(TimeLog.username == username)
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
    msg = f"""total work time spent by user {username} from {start_time_cut} to {end_time} on epic {epic_name} is {work_time_sum}
            """
    return msg
