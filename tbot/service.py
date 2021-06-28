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
    KeyboardButton(msg.btn_video),
    KeyboardButton(msg.btn_image),

)

TRANSFER_KB = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).row(
    KeyboardButton(msg.style_1),
    KeyboardButton(msg.style_2),
    KeyboardButton(msg.style_3),
    KeyboardButton(msg.style_4),
    KeyboardButton(msg.style_5),
)



