import io
import logging
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import Dispatcher

import config
import tbot.service as s
from tbot.dialogs import Messages as msg
from database import cache
from tbot.antiflood import *
from tbot.states import *
from utils import get_data, get_prediction, postprocessing
import base64
import numpy as np

from video import video_main
from video.video_main import download_video

bot = Bot(token=config.TOKEN)
storage = RedisStorage2(db=5,
                        host=config.REDIS_HOST,
                        port=config.REDIS_PORT,
                        password=config.REDIS_PASSWORD)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(ThrottlingMiddleware())

GAN = video_main.gan_t()


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    """Обработка команды start. Вывод текста и меню"""
    await message.answer(msg.start_current_user.format(name=message.from_user.first_name),
                         reply_markup=s.MAIN_KB)


@dp.message_handler(content_types=['photo', 'document'])
@rate_limit(5, 'photo_video')
async def handle_docs_photo(message: types.Message):
    """Обработка команды start. Вывод текста и меню"""
    if message.content_type == 'photo':
        img = message.photo[-1]
    else:
        img = message.document
        print(img.mime_type[:500])
        if img.mime_type[:5] != 'image':
            await bot.send_message(message.chat.id,
                                   "Загрузи, пожалуйста, файл в формате изображения.",
                                   reply_markup=s.MAIN_KB)
    cache.setex(f"last_message_{message.from_user.id}", config.HOUR, img.file_unique_id)
    if cache.get(f"{img.file_unique_id}") is None:
        await img.download(f'temp/{message.message_id}.jpg')
        photo, shape = await get_data(f'temp/{message.message_id}.jpg')
        cache.setex(f"{img.file_unique_id}", config.HOUR, base64.b64encode(photo).decode("utf-8"))
        cache.setex(f"{img.file_unique_id}_shape", config.HOUR, str(shape))

        await message.answer("Картинка норм, теперь выбери стиль",
                             reply_markup=s.TRANSFER_KB)
    # TODO: через state aiogram


@dp.message_handler(
    lambda message: message.text in (msg.style_1, msg.style_2, msg.style_3, msg.style_4, msg.style_5))
async def processing(message: types.Message):
    if cache.get(f"last_message_{message.from_user.id}") is None:
        await bot.send_message(message.chat.id,
                               "Сначало загрузи, пожалуйста, файл в формате изображения.",
                               reply_markup=s.MAIN_KB)

        """Image processing depending on the selected style."""
    else:
        photo_id = cache.get(f"last_message_{message.from_user.id}")
        photo = cache.get(photo_id).encode('utf8')
        r = base64.decodebytes(photo)
        q = np.frombuffer(r, dtype=np.float32)
        temp_img = await get_prediction(q, message.text)
        photo_org_size = cache.get(f'{photo_id}_shape')
        result_image = await postprocessing(temp_img, photo_org_size)

    await message.answer(text='Processing has started and will take some time. '
                              'Wait for a little bit.',
                         reply_markup=types.ReplyKeyboardRemove())

    imgByteArr = io.BytesIO()
    result_image.save(imgByteArr, format='JPEG', compress_level=9)
    imgByteArr = imgByteArr.getvalue()

    await message.answer_photo(imgByteArr, caption='Done!')


@dp.message_handler(commands=['cancel'])
async def help_handler(message: types.Message):
    """Обработка команды cancel. Вывод текста и меню"""
    await message.answer(msg.cancel, reply_markup=s.MAIN_KB)


@dp.message_handler(lambda message: message.text == msg.btn_video)
async def video_handler(message: types.Message):
    """Обработка сообщения Видео. Вывод текста и ожидание видео"""
    await message.answer(
        text='Вы выбрали обработку видео, ожидаю ссылку на тикток, вся обработка занимает около минуты',
        reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == msg.btn_image)
async def image_handler(message: types.Message):
    """Обработка сообщения Изображения. Вывод текста и ожидание картинки"""
    await message.answer(text='Вы выбрали обработку изображения, ожидаю картинку',
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['help'])
@dp.message_handler(lambda message: message.text.lower() in ['help'])
async def help_handler(message: types.Message):
    """Обработка команды help. Вывод текста и меню"""
    await message.answer(msg.help, reply_markup=s.MAIN_KB)


@dp.message_handler(lambda message: set([item.url for item in message.entities]).isdisjoint(["url", 'textlink']))
async def video_message(message: types.Message):
    """Ответ на любую ссылку тиктока """
    for item in message.entities:
        if item.type in ['url', 'textlink']:
            await bot.send_message(message.chat.id,
                                   f"загружаю видео - {message.text}",
                                   reply_markup=types.ReplyKeyboardRemove())
            async with asyncio.Lock():
                video_path = download_video(message.text)
            await bot.send_message(message.chat.id,
                                   "начинаю обработку",
                                   reply_markup=types.ReplyKeyboardRemove())
            async with asyncio.Lock():
                GAN.video(video_path)
            await message.answer_video(open(f'./output/{video_path}.mp4', 'rb'))


@dp.message_handler()
async def unknown_message(message: types.Message):
    """Ответ на любое неожидаемое сообщение"""
    await message.answer(msg.unknown_text, reply_markup=s.MAIN_KB)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
