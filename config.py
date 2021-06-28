import pathlib
import os
import ujson
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN", "869189726:AAF89Zu05Stln1ZP7G8weTyDJvbB3I3fpFs")
BOT_VERSION = 1

# Данные redis-клиента
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None

# time
MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24
WEEK = DAY * 7
YEAR = WEEK * 55

MODELS = {str(idx+1): str(path) for idx, path in enumerate([p for p in pathlib.Path('./models').iterdir() if p.is_file()])}
print(MODELS)
