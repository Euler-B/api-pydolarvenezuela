import telebot
from datetime import datetime
from ._base import Storage
from ..consts import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

class TelegramStorage(Storage):
    def __init__(self):
        self.bot = telebot.TeleBot(TELEGRAM_TOKEN)

    def upload(self, file: str) -> None:
        date_str = datetime.now().strftime('%Y-%m-%d')
        with open(file, 'rb') as file:
            self.bot.send_document(chat_id=TELEGRAM_CHAT_ID, document=file, caption=f'Backup {date_str}.sql')