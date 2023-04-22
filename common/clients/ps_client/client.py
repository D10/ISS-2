import psycopg2

from common.base import logger

from common.clients.ps_client.ps_queries import GET_USER_BY_ID, GET_USER_BY_ACCESS_KEY, GET_ROUTER_CONFIG
from common.clients.ps_client.ps_models import User, RouterConfig

DATABASE = 'iss'
USER = 'dio'
PASSWORD = '132435'


class Client:
    
    def __init__(self):
        self.connection = psycopg2.connect(
                dbname=DATABASE,
                user=USER,
                password=PASSWORD
            )
        logger.info('ps_client Created')
        
    
    def _fetchone(self, query, cursor, clss):
        logger.info(f'Request to ps_client. {query}')
        try:
            cursor.execute(query)
            response = cursor.fetchone()
            response = clss(*response) if response else None
            logger.info(f'Response from ps_client. {response}')
            return response
        except Exception as ex:
            logger.error(f'ps_client request error! {ex}')
    
    def _fetchall(self, query, cursor, clss):
        logger.info(f'Request to ps_client. {query}')
        try:
            cursor.execute(query)
            response = cursor.fetchall()
            response = [clss(*obj) for obj in response] if response else None
            return response
        except Exception as ex:
            logger.error(f'ps_client request error! {ex}')
    
    def get_user_by_id(self, id, cursor=None, clss=User):
        return self._fetchone(GET_USER_BY_ID %id, cursor, clss)
    
    def get_user_by_access_key(self, key, cursor=None, clss=User):
        return self._fetchone(GET_USER_BY_ACCESS_KEY %key, cursor, clss)
    
    def get_router_config(self, id=1, cursor=None, clss=RouterConfig):
        return self._fetchone(GET_ROUTER_CONFIG %id, cursor, clss)


if __name__ == '__main__':
    ps_client = Client()
    
    with ps_client.connection.cursor() as cursor:
        user = ps_client.get_user_by_id(1, cursor=cursor)
        print(user.name)
        
