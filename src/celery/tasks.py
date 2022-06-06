from src.open_weather.api import OpenWeather
from src.celery.app import celery_app
from src import db_schedule
from src.tg import tg_bot

import datetime


@celery_app.task
def send_notification():
    time_now = datetime.datetime.now()
    time_now = f'{time_now.hour}.{time_now.minute}'
    schedules = db_schedule.get_schedules_by_schedule_time(time_now)
    for schedule in schedules:
        city = schedule[2]
        tg_bot.send_message(schedule[4], OpenWeather(city).weather_str())


@celery_app.task
def start_bot_task():
    print(1)
    from src.tg import handlers
    print(2)
    tg_bot.polling(none_stop=True, interval=0)
    print(3)
