import logging

SLACK_CHANNEL_NAME = '#iss-alerts'
ROCKET_CHANNEL_NAME = 'iss-alerts'

ROCKET_HOST = 'http://192.168.180.91:3000'

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler('logs/iss_logs.log', 'a', 'utf-8')],
    format="LEVEL===%(levelname)s TIMESTAMP===%(asctime)s TEXT===%(message)s"
)

logger = logging.getLogger('iss_logger')
