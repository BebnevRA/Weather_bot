import datetime

from telebot import types

from src.open_weather.api import OpenWeather
from src.tg.config import COUNT_FOR_BAN
from src.tg.bot import tg_bot
from src.tg import messages
from src import db_check_ip as db, db_ban_list
from src.tg import keyboards


@tg_bot.message_handler(commands=["start"])
def start(m):
    tg_bot.send_message(m.chat.id, messages.HELLO_MESSAGE,
                        reply_markup=keyboards.start_keyboard)


@tg_bot.message_handler(commands=["schedule"])
def schedule(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("1")
    item2 = types.KeyboardButton("2")
    item3 = types.KeyboardButton("3")
    item4 = types.KeyboardButton("4")
    markup.row(item1, item2)
    markup.add(item3)
    tg_bot.send_message(m.chat.id, 'щас будем делать расписание',
                        reply_markup=keyboards.test_keyboard)


@tg_bot.callback_query_handler(func=lambda c: c.data == 'button1')
def test(callback_query: types.CallbackQuery):
    tg_bot.answer_callback_query(callback_query.id)
    tg_bot.send_message(callback_query.from_user.id, 'take button1',
                        reply_markup=keyboards.test_keyboard2)


@tg_bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('but'))
def test2(callback_query: types.CallbackQuery):
    print(callback_query.data)
    code = callback_query.data[-1]
    print(code)
    if code.isdigit():
        code = int(code)
    if code == 2:
        tg_bot.answer_callback_query(callback_query.id, text='Нажата button2')
    elif code == 3:
        tg_bot.answer_callback_query(
            callback_query.id,
            text='Нажата button3.\nА этот текст может быть длиной до 200 символов 😉', show_alert=True)
    else:
        tg_bot.answer_callback_query(callback_query.id)
    # tg_bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')


@tg_bot.message_handler(content_types=['text'])
def handle_text(message):
    if db_ban_list.get(message.from_user.username):
        tg_bot.send_message(message.chat.id, messages.BAN_MESSAGE)
        return
    check_on_spam(username=message.from_user.username)

    # print('id - ', message.chat.id)
    # print('Никнейм - ', message.from_user.username)
    # print('Имя - ', message.from_user.first_name)

    weather = OpenWeather(message.text)
    if weather.error_message:
        tg_bot.send_message(message.chat.id, weather.error_message)
    else:
        tg_bot.send_message(message.chat.id, weather.weather_str(),
                            reply_markup=keyboards.share_button(
                                weather.weather_str()))


def check_on_spam(username):
    # now = datetime.datetime.now()
    # username = 'etroks'
    #
    # username_min = f'{username}-{now.minute}'
    # count = r.incr(username_min)
    # if count < COUNTFORBAN:
    #     print(r.expire(username_min, 60))
    # else:
    #     print('BAN ' + username)

    now = datetime.datetime.now()
    time = f'{now.minute}.{now.second}'

    db.lpush(username, time)
    if db.llen(username) == COUNT_FOR_BAN:
        delta = float(db.lindex(username, 0)) - float(db.lindex(username, -1))

        if delta < -59 or delta < 1:
            db_ban_list.set(username,
                            f'{now.day}.{now.month}.{now.year} '
                            f'- {now.hour}.{now.minute}')
        else:
            db.rpop(username)


if __name__ == '__main__':
    tg_bot.polling(none_stop=True, interval=0)
