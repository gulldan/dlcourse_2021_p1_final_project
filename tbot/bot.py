import logging
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher

from config import TOKEN, YEAR, MINUTE
import tbot.service as s
from tbot.dialogs import Messages as msg
from database import cache

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    """Обработка команды start. Вывод текста и меню"""
    await message.answer(msg.start_current_user.format(name=message.from_user.first_name),
                         reply_markup=s.MAIN_KB)


@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    """Обработка команды help. Вывод текста и меню"""
    await message.answer(msg.help, reply_markup=s.MAIN_KB)


@dp.callback_query_handler(lambda c: c.data == 'main_window')
async def show_main_window(callback_query: types.CallbackQuery):
    """Главный экран"""
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, msg.main, reply_markup=s.MAIN_KB)


@dp.callback_query_handler(lambda c: c.data.startswith('update_results'))
async def update_results(callback_query: types.CallbackQuery):
    """Обновление сообщения результатов"""
    if cache.get(f"last_update_{callback_query.from_user.id}") is None:
        user_leagues = callback_query.data.split("#")[1:]
        answer = await s.generate_results_answer(user_leagues)
        cache.setex(f"last_update_{callback_query.from_user.id}", MINUTE, "Updated")
        await bot.edit_message_text(
            answer,
            callback_query.from_user.id,
            message_id=int(cache.get(f"last_msg_{callback_query.from_user.id}"))
        )
    # игнорируем обновление, если прошло меньше минуты
    await callback_query.answer(msg.cb_updated)


@dp.message_handler()
async def unknown_message(message: types.Message):
    """Ответ на любое неожидаемое сообщение"""
    await message.answer(msg.unknown_text, reply_markup=s.MAIN_KB)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
