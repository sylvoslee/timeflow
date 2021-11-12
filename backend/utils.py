import datetime


def string_to_datetime(date_string):
    date = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date


def initials(full_name):
    bname = full_name.strip()
    lenofstr = len(bname)
    fname = bname[0]
    leofstrstr = str(lenofstr)
    vlname = int(lenofstr) - 5
    lname = bname[int(vlname)]
    initials = fname[0] + lname[0]
    return initials
