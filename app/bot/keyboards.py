from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import ALL_SERVICE_NAMES


def create_keyboard(button_names: Iterable, row_width: int):
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = row_width

    for button_name in button_names:
        keyboard.insert(InlineKeyboardButton(text=button_name,
                                             callback_data=button_name))

    return keyboard


start_keyboard = create_keyboard(button_names=ALL_SERVICE_NAMES, row_width=2)
