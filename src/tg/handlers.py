import datetime

from src.open_weather.api import OpenWeather
from src.tg.config import COUNT_FOR_BAN
from src.tg.bot import tg_bot
from src.tg import messages
from src import db_check_ip, db_ban_list, db_schedule
from src.tg import keyboards


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
    schedule = db_schedule.smembers(m.from_user.username)
    if schedule:
        message = 'Ваши уведомления:'
        for time in schedule:
            message += f'\n{time.decode("utf-8")}'
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
        time_format = '%H.%M'
        time = datetime.datetime.strptime(m.text, time_format)
        db_schedule.sadd(m.from_user.username,
                         f'{city_name}-{time.hour}.{time.minute}')
        tg_bot.send_message(m.chat.id, text=messages.SUCCESS_MESSAGE)
        # отправка задачи в сентри
    except ValueError:
        msg = tg_bot.send_message(m.chat.id,
                                  text=messages.ERROR_ENTERING_MESSAGE)
        tg_bot.register_next_step_handler(msg, new_schedule_st3, city_name)


@tg_bot.message_handler(commands=["del_schedule"])
def del_schedule(m):
    schedules = db_schedule.smembers(m.from_user.username)
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
        if schedule.decode("utf-8").split('-')[0] == del_city:
            city_counter += 1

    if city_counter == 0:
        msg = tg_bot.send_message(m.chat.id,
                                  text=messages.NO_CITY_DEL_SCHEDULE_MESSAGE)
        tg_bot.register_next_step_handler(msg, del_schedule_st2, schedules)
    elif city_counter == 1:
        for schedule in schedules:
            if schedule.decode("utf-8").split('-')[0] == del_city:
                db_schedule.srem(m.from_user.username, schedule)
                # удаление задачи из сентри
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
        time_format = '%H.%M'
        time = datetime.datetime.strptime(m.text, time_format)
        result = db_schedule.srem(m.from_user.username,
                                  f'{del_city}-{time.hour}.{time.minute}')
        if result:
            tg_bot.send_message(m.chat.id, text=messages.SUCCESS_MESSAGE)
            # удаление задачи из сентри
        else:
            msg = tg_bot.send_message(m.chat.id,
                                      text=messages.N0_SCHEDULE_VALUE_MESSAGE)
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
    now = datetime.datetime.now()
    time = f'{now.minute}.{now.second}'

    db_check_ip.lpush(username, time)
    if db_check_ip.llen(username) == COUNT_FOR_BAN:
        delta = float(db_check_ip.lindex(username, 0)) - \
                float(db_check_ip.lindex(username, -1))

        if delta < -59 or delta < 1:
            db_ban_list.set(username,
                            f'{now.day}.{now.month}.{now.year} '
                            f'- {now.hour}.{now.minute}',
                            keepttl=60)
        else:
            db_check_ip.rpop(username)


if __name__ == '__main__':
    tg_bot.polling(none_stop=True, interval=0)
