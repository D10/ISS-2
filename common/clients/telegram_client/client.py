import telebot

from common.base import logger


class Client:
    
    def __init__(self, token, chat_id):
        self.bot = telebot.TeleBot(token)
        self.chat_id = chat_id
    
    def send_message(self, text=None):
        try:
            logger.info('Request to telegram - send message')
            self.bot.send_message(chat_id=self.chat_id, text=text)
        except telebot.apihelper.ApiTelegramException as e:
            logger.error(f'Telegram request error! {e}')
        else:
            logger.info(f'Successfully sent message "{text}"')


if __name__ == '__main__':
    client = Client()
    client.send_message()
