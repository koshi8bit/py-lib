import os
import time
from unittest import TestCase
from dotenv import load_dotenv
from lib.koshi8bit.telegram_my import TelegramMy


class TestTelegramMy(TestCase):
    def test_start_logging(self):
        load_dotenv()
        telega = TelegramMy(os.getenv('TELEGRAM_TOKEN'), os.getenv('TELEGRAM_CHAT_ID'))
        telega.set_project_prefix(os.getenv('TELEGRAM_PREFIX'))
        telega.send('test_start_logging')

        telega.start_logging(5)
        time.sleep(1)
        telega.commit('1')
        time.sleep(1)
        telega.commit('2')
        time.sleep(5)
        telega.commit('3')
        time.sleep(5)
        telega.disconnect()

    def test_send_to_file(self):
        load_dotenv()
        telega = TelegramMy(os.getenv('TELEGRAM_TOKEN'), os.getenv('TELEGRAM_CHAT_ID'))
        telega.set_project_prefix(os.getenv('TELEGRAM_PREFIX'))
        telega.send('test_send_to_file')
        telega.send('a'*5000)
        telega.disconnect()
