import telebot

from src.config import TG_BOT_TOKEN, TIMEZONE_OFFSET
from src.open_weather.api import OpenWeather
from src.celery.app import celery_app
from src import db_schedule

import datetime


@celery_app.task
def send_notification():
    tg_bot = telebot.TeleBot(TG_BOT_TOKEN)

    time_now = datetime.datetime.now(TIMEZONE_OFFSET)
    time_now = f'{time_now.hour}.{time_now.minute}'
    schedules = db_schedule.get_schedules_by_schedule_time(time_now)

    if schedules is None:
        return

    for schedule in schedules:
        city = schedule[2]
        tg_bot.send_message(schedule[4], OpenWeather(city).weather_str())

