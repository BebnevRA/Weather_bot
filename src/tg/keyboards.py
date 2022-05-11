from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton("Москва"),
    types.KeyboardButton("Санкт-Петербург"),
)
start_keyboard.row(
    types.KeyboardButton("Составить расписание")
)
# one_time_keyboard=True убирать клавишу поле нажатия


test_keyboard = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton('button1', callback_data='button1')
)


def share_button(message):
    button = InlineKeyboardMarkup().add(
        InlineKeyboardButton('Скорее рассказать об этом', switch_inline_query=message))
    return button


test_keyboard2 = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton('button2', callback_data='button2'),
    types.InlineKeyboardButton('button3', callback_data='button3'),
    types.InlineKeyboardButton('button4', callback_data='button4')
)




# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
# inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
# inline_kb_full.add(InlineKeyboardButton('Вторая кнопка', callback_data='btn2'))
# inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')
# inline_btn_4 = InlineKeyboardButton('кнопка 4', callback_data='btn4')
# inline_btn_5 = InlineKeyboardButton('кнопка 5', callback_data='btn5')
# inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
# inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)
# inline_kb_full.insert(InlineKeyboardButton("query=''", switch_inline_query=''))
# inline_kb_full.insert(InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'))
# inline_kb_full.insert(InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd'))
# inline_kb_full.add(InlineKeyboardButton('Уроки aiogram', url='https://surik00.gitbooks.io/aiogram-lessons/content/'))


test_keyboard3 = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("query=''", switch_inline_query=''),
    InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'),
    InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd')
)
