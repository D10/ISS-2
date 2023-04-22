import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from common.base import SLACK_CHANNEL_NAME
from common.base import logger


class Client:

    def __init__(self, token):
        try:
            self.s_client = WebClient(token=token)
        except KeyError:
            logger.error('BOT TOKEN NOT FOUND!')
        except SlackApiError:
            logger.error('Invalid token!')

    def send_message(self, text='Test message'):
        try:
            logger.info(f'Request to slack - send message')
            response = self.s_client.chat_postMessage(channel=SLACK_CHANNEL_NAME, text=text)
        except SlackApiError as e:
            logger.error(f'Slack request error! {e.response["error"]}')
        else:
            logger.info(f'Successfully sent message "{text}"')


if __name__ == '__main__':
    s_client = Client()
    s_client.send_message()
