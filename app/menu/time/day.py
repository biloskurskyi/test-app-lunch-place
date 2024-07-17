from datetime import datetime

import requests


def get_current_day_kiev():
    response = requests.get("http://worldtimeapi.org/api/timezone/Europe/Kiev")
    if response.status_code == 200:
        data = response.json()
        return data['day_of_week'] - 1
    else:
        return None


def get_time_in_kiev():
    response = requests.get("http://worldtimeapi.org/api/timezone/Europe/Kiev")
    if response.status_code == 200:
        data = response.json()
        return data['datetime']
    else:
        return None


def get_hour_from_datetime(datetime_str):
    if datetime_str:
        dt = datetime.fromisoformat(datetime_str)
        return dt.hour
    else:
        return None


live_time_in_kiev = get_time_in_kiev()
hour_in_kiev = get_hour_from_datetime(live_time_in_kiev)
