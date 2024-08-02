import datetime
import pytz


def current_timestamp():
    return int(datetime.datetime.now(pytz.timezone("Asia/Tehran")).timestamp())
