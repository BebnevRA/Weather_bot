from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.tg import messages


def default_keyboard(first_button='Москва', second_button='Санкт-Петербург'):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        types.KeyboardButton(first_button),
        types.KeyboardButton(second_button),
    )

    return keyboard


def share_button(message):
    button = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text=messages.SHARE_MESSAGE,
                             switch_inline_query=message))
    return button

