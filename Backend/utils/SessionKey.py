from datetime import datetime, timedelta
import time


def get_session_key():
    now = datetime.now()
    current_hour_start = now.replace(minute=0, second=0, microsecond=0)
    next_hour_start = current_hour_start + timedelta(hours=1)

    interval_key = f"{int(time.mktime(current_hour_start.timetuple()))}-{int(time.mktime(next_hour_start.timetuple()))}"
    return interval_key
