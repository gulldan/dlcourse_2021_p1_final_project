import os
import logging
import redis
import ujson
import config


class Cache(redis.StrictRedis):
    def __init__(self, host, port, password,
                 charset="utf-8",
                 decode_responses=True):
        super(Cache, self).__init__(host, port,
                                    password=password,
                                    charset=charset,
                                    decode_responses=decode_responses)
        logging.info("Redis start")

    def jset(self, name, value, ex=0):
        """функция конвертирует python-объект в Json и сохранит"""
        r = self.get(name)
        if r is None:
            return r
        return ujson.loads(r)

    def jget(self, name):
        """функция возвращает Json и конвертирует в python-объект"""
        return ujson.loads(self.get(name))


# создание объектов cache
cache = Cache(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD
)
