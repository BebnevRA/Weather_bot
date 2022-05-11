from src.celery.app import celery_app
import time

import telebot
import datetime


@celery_app.task
def add(x, y):
    return x + y


@celery_app.task
def start_bot_task():
    # from src.tg import test, bot
    # bot.tg_bot.polling(none_stop=True, interval=0)
    from src.tg import handlers
    from src.tg.bot import tg_bot
    tg_bot.polling(none_stop=True, interval=0)


@celery_app.task
def wait():
    time.sleep(30)


@celery_app.task
def test_task():
    now = datetime.datetime.now()
    time = f'{now.hour}.{now.minute}.{now.second}'
    bot = telebot.TeleBot('5295909082:AAGv4Ac6987pH5xXjCeSEm_wEeYtFud12yM')
    bot.send_message('297452818', f'Сейчас уже {time}')
    return True



