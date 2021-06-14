from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize
from config import MINUTE
from database import cache
from tbot.dialogs import Messages as msg

MAIN_KB = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).row(
    KeyboardButton(msg.btn_online),
    KeyboardButton(msg.btn_config)
)

CONFIG_KB = InlineKeyboardMarkup().row(
    InlineKeyboardButton(msg.config_btn_edit, callback_data='edit_config#')
)


def results_to_text(matches: list) -> str:
    """
    Функция генерации сообщения
    """
    # логику напишем в следующей части

    return ''
