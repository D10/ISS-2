from common.clients.ps_client import client as ps_client
from common.clients.rocketchat_client import rocket_client
from common.clients.slack_client import client as slack_client
from common.clients.telegram_client import client as telegram_client

from common.base import logger


class Router:
    
    def __init__(self):
        pss_client = ps_client.Client()
        with pss_client.connection.cursor() as cursor:
            self.config = pss_client.get_router_config(cursor=cursor)
        
        
        self.integrations = []
        
        if self.config:
            if self.config.slack_integration:
                self.slack = slack_client.Client(self.config.slack_token)
                self.integrations.append(self.slack)
            if self.config.rocket_integration:
                self.rocket = rocket_client.Client(self.config.rocket_login, self.config.rocket_password)
                self.integrations.append(self.rocket)
            if self.config.telegram_integration:
                self.telegram = telegram_client.Client(self.config.telegram_token, self.config.telegram_chat_id)
                self.integrations.append(self.telegram)
        
        logger.info('Init message router')
    
    def send_message(self, text='test_message'):
        if self.integrations:
            for integration in self.integrations:
                integration.send_message(text)
        
