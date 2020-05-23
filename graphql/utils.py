import datetime

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)

def today_datetime_start():
    return datetime.datetime.combine(datetime.datetime.today(), datetime.time(0,0,0))

def today_datetime_end():
    return datetime.datetime.combine(datetime.datetime.today(), datetime.time(23,59,59))