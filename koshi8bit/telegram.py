import traceback

import telegram
import io
import datetime


class TelegramMy:
    def __init__(self, bot_token, chat_id):
        self.bot = telegram.Bot(token=bot_token)
        self.chat_id = chat_id
        self.project_prefix = None

    def set_project_prefix(self, text):
        if text == '':
            return

        self.project_prefix = f'*{text}*'

    def send(self, text, raise_exception=True):
        if len(text) > 4095:  # telegram max 4096
            self.send_text_as_file(text)
        try:
            if self.project_prefix is not None:
                text = f'{self.project_prefix}: {text}'

            self.bot.sendMessage(chat_id=self.chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

        except Exception as ex:
            if raise_exception:
                raise ex

    def send_text_as_file(self, text, file_name=None, raise_exception=True):
        try:
            if file_name is None:
                now = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%f")
                file_name = f'{now}.log'
            file = io.StringIO(text)
            file.name = file_name
            result = self.bot.sendDocument(self.chat_id, document=file)

        except Exception as ex:
            if raise_exception:
                raise ex

    def send_stack(self, text, raise_exception=True):
        try:
            self.send(text)
            self.send_text_as_file(traceback.format_exc())

        except Exception as ex:
            if raise_exception:
                raise ex
