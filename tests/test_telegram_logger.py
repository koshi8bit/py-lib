import os
import time
from unittest import TestCase
from dotenv import load_dotenv
from lib.koshi8bit.telegram_logger import TelegramLogger


class TestTelegramMy(TestCase):
    def __init__(self, argv):
        super().__init__(argv)
        load_dotenv()
        self.tg = TelegramLogger(os.getenv('TELEGRAM_TOKEN'), os.getenv('TELEGRAM_CHAT_ID'))
        self.tg.set_project_prefix(os.getenv('TELEGRAM_PREFIX'))

    def test_start_logging(self):
        self.tg.send('test_start_logging')

        self.tg.start_pushing(5)
        time.sleep(1)
        self.tg.commit('1')
        time.sleep(1)
        self.tg.commit('2')

        time.sleep(5)
        self.tg.commit('3')
        time.sleep(5)
        self.tg.disconnect()

    def test_send_to_file(self):
        self.tg.send('test_send_to_file')
        self.tg.send('a'*5000)
        self.tg.disconnect()

    def test_send_stack_with_text(self):
        try:
            raise ValueError("test error (with_text)")
        except Exception as e:
            self.tg.send_stack("test ex")

        self.tg.disconnect()

    def test_send_stack_without_text(self):
        try:
            raise ValueError("test error (without_text)")
        except Exception as e:
            self.tg.send_stack()

        self.tg.disconnect()
