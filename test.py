import unittest
import aiohttp
from unittest import IsolatedAsyncioTestCase

from database import cache
from tbot import bot


class TestCache(unittest.TestCase):
    def test_connection(self):
        self.assertTrue(cache.ping())

    def test_response_type(self):
        cache.setex("test_type", 10, "Hello")
        response = cache.get("test_type")
        self.assertEqual(type(response), str)


class TestBot(IsolatedAsyncioTestCase):
    async def test_bot_auth(self):
        bot.bot._session = aiohttp.ClientSession()
        bot_info = await bot.bot.get_me()
        await bot.bot._session.close()
        self.assertEqual(bot_info["username"], "mk_usefull_bot")


if __name__ == '__main__':
    unittest.main()
