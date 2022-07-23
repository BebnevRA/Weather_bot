import datetime
import re

from src.open_weather.api import OpenWeather
from src.config import COUNT_FOR_BAN, TIMEZONE_OFFSET
from src.tg import tg_bot, messages, keyboards
from src import db_check_ip, db_ban_list, db_schedule


@tg_bot.message_handler(commands=["start"])
def start(m):
    tg_bot.send_message(m.chat.id, text=messages.HELLO_MESSAGE,
                        reply_markup=keyboards.default_keyboard())


@tg_bot.message_handler(commands=["help"])
def help(m):
    tg_bot.send_message(m.chat.id, text=messages.HELP_MESSAGE)


@tg_bot.message_handler(commands=["change_default_cities"])
def change_default_cities(m):
    msg = tg_bot.send_message(m.chat.id,
                              text=messages.CHANGE_FIRST_CITY_MESSAGE)
    tg_bot.register_next_step_handler(msg, change_first_city)


def change_first_city(m):
    msg = tg_bot.send_message(m.chat.id,
                              text=messages.CHANGE_SECOND_CITY_MESSAGE)
    tg_bot.register_next_step_handler(msg, change_second_city, m.text)


def change_second_city(m, first_city_name):
    tg_bot.send_message(m.chat.id, text=messages.SUCCESS_MESSAGE,
                        reply_markup=keyboards.default_keyboard(
                                  first_city_name, m.text))


@tg_bot.message_handler(commands=["my_schedule"])
def my_schedule(m):
    schedules = db_schedule.get_schedules_by_username(m.from_user.username)
    if schedules:
        message = 'Ваши уведомления:'
        for schedule in schedules:
            message += f'\n{schedule[2]}-{schedule[3]}'
    else:
        message = messages.NO_SCHEDULE_MESSAGE
    tg_bot.send_message(m.chat.id, text=message)


@tg_bot.message_handler(commands=["new_schedule"])
def new_schedule(m):
    msg = tg_bot.send_message(m.chat.id,
                              text=messages.ADDING_CITY_SCHEDULE_MESSAGE)
    tg_bot.register_next_step_handler(msg, new_schedule_st2)


def new_schedule_st2(m):
    if m.text == 'Отмена' or m.text == 'отмена':
        return

    city_name = m.text
    if OpenWeather(city_name).is_valid_city_name():
        msg = tg_bot.send_message(m.chat.id,
                                  text=messages.ADDING_TIME_SCHEDULE_MESSAGE)
        tg_bot.register_next_step_handler(msg, new_schedule_st3, city_name)
    else:
        msg = tg_bot.send_message(m.chat.id,
                                  text=messages.ERROR_ENTERING_MESSAGE)
        tg_bot.register_next_step_handler(msg, new_schedule_st2)


def new_schedule_st3(m, city_name):
    if m.text == 'Отмена' or m.text == 'отмена':
        return

    try:
        if re.match(r"^[0-2][0-9].[0-5][0-9]$", m.text):
            if db_schedule.get_schedule(username=m.from_user.username,
                                        city=city_name,
                                        schedule_time=m.text,
                                        chat_id=m.chat.id):
                tg_bot.send_message(m.chat.id, text=messages.SCHEDULE_ALREADY_EXIST)
            else:
                db_schedule.add_schedule(
                    username=m.from_user.username, city=city_name,
                    schedule_time=f'{m.text.split(".")[0]}.{m.text.split(".")[1]}',
                    chat_id=m.chat.id)
                tg_bot.send_message(m.chat.id, text=messages.SUCCESS_MESSAGE)
        else:
            tg_bot.send_message(m.chat.id, text=messages.ERROR_ENTERING_MESSAGE)
    except ValueError:
        msg = tg_bot.send_message(m.chat.id,
                                  text=messages.ERROR_ENTERING_MESSAGE)
        tg_bot.register_next_step_handler(msg, new_schedule_st3, city_name)


@tg_bot.message_handler(commands=["del_schedule"])
def del_schedule(m):
    schedules = db_schedule.get_schedules_by_username(m.from_user.username)
    if not schedules:
        tg_bot.send_message(m.chat.id, text=messages.NO_SCHEDULE_MESSAGE)
        return

    msg = tg_bot.send_message(m.chat.id,
                              text=messages.DEL_SCHEDULE_CITY_MESSAGE)
    tg_bot.register_next_step_handler(msg, del_schedule_st2, schedules)


def del_schedule_st2(m, schedules):
    if m.text == 'Отмена' or m.text == 'отмена':
        return

    del_city = m.text
    city_counter = 0
    for schedule in schedules:
        if schedule[2] == del_city:
            city_counter += 1

    if city_counter == 0:
        msg = tg_bot.send_message(m.chat.id,
                                  text=messages.NO_CITY_DEL_SCHEDULE_MESSAGE)
        tg_bot.register_next_step_handler(msg, del_schedule_st2, schedules)
    elif city_counter == 1:
        for schedule in schedules:
            if schedule[2] == del_city:
                db_schedule.del_schedule_by_username_and_city(
                    username=m.from_user.username, city=schedule[2])
                tg_bot.send_message(m.chat.id,
                                    text=messages.SUCCESS_MESSAGE)
                return
    else:
        msg = tg_bot.send_message(m.chat.id,
                                  text=messages.DEL_SCHEDULE_TIME_MESSAGE)
        tg_bot.register_next_step_handler(msg, del_schedule_st3,
                                          schedules, del_city)


def del_schedule_st3(m, schedules, del_city):
    if m.text == 'Отмена' or m.text == 'отмена':
        return

    try:
        if re.match(r"^[0-2][0-9].[0-5][0-9]$", m.text):
            if db_schedule.del_schedule_by_username_city_time(
                    username=m.from_user.username, city=del_city, time=m.text):
                tg_bot.send_message(m.chat.id, text=messages.SUCCESS_MESSAGE)
            else:
                msg = tg_bot.send_message(m.chat.id,
                                          text=messages.N0_SCHEDULE_VALUE_MESSAGE)
                tg_bot.register_next_step_handler(msg, del_schedule_st3,
                                                  schedules, del_city)
        else:
            msg = tg_bot.send_message(m.chat.id,
                                      text=messages.ERROR_ENTERING_MESSAGE)
            tg_bot.register_next_step_handler(msg, del_schedule_st3,
                                              schedules, del_city)
    except ValueError:
        msg = tg_bot.send_message(m.chat.id,
                                  text=messages.ERROR_ENTERING_MESSAGE)
        tg_bot.register_next_step_handler(msg, del_schedule_st3,
                                          schedules, del_city)


@tg_bot.message_handler(content_types=['text'])
def handle_text(message):
    if db_ban_list.get(message.from_user.username):
        tg_bot.send_message(message.chat.id, text=messages.BAN_MESSAGE)
        return
    check_on_spam(username=message.from_user.username)

    weather = OpenWeather(message.text)
    if weather.is_valid_city_name():
        tg_bot.send_message(message.chat.id, weather.weather_str(),
                            reply_markup=keyboards.share_button(
                                weather.weather_str()))
    else:
        tg_bot.send_message(message.chat.id, weather.error_message)


def check_on_spam(username):
    now = datetime.datetime.now(TIMEZONE_OFFSET)
    time = f'{now.minute}.{now.second}'

    db_check_ip.lpush(username, time)
    if db_check_ip.llen(username) == COUNT_FOR_BAN:
        delta = float(db_check_ip.lindex(username, 0)) - \
                float(db_check_ip.lindex(username, -1))

        if delta < -59 or delta < 1:
            db_ban_list.set(username,
                            f'{now.day}.{now.month}.{now.year} '
                            f'- {now.hour}.{now.minute}',
                            ex=600)
            db_check_ip.delete(username)
        else:
            db_check_ip.rpop(username)


if __name__ == '__main__':
    print('start')
    tg_bot.polling(none_stop=True)
