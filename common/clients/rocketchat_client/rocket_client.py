from rocketchat_API.rocketchat import RocketChat

from common.base import logger, ROCKET_HOST, ROCKET_CHANNEL_NAME


class Client:
    def __init__(self, login, password):
        logger.info(f'login={login}  pass={password}')
        try:
            self.client = RocketChat(
                login,
                password,
                server_url=ROCKET_HOST
            )
        except Exception as e:
            logger.error(f'Error rocket client! {e}') 
    
    def send_message(self, text='test message'):
        try:
            logger.info('Request to rocket - send message')
            posted_message = self.client.chat_post_message(
                room_id=ROCKET_CHANNEL_NAME,
                text=text
            )
        except Exception as e:
            logger.error(f'Rocket request error! {e}')
        else:
            logger.info(f'Successfully sent message "{text}"')
            


if __name__ == '__main__':
    client = Client()
    client.send_message()
