# docker run --name redis --rm -p 6379:6379 -d redis:alpine

from aiogram import executor
from tbot import bot
executor.start_polling(bot.dp,
                       skip_updates=True,
                       on_shutdown=bot.on_shutdown)