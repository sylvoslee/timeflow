import datetime


def string_to_datetime(date_string):
    date = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date
