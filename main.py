import time

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from common.clients.ps_client import client as ps_client
from common import router

from common.base import logger

from sensor_modules.alarm import signal_point
from sensor_modules.led import LED

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

ps_client = ps_client.Client()
router = router.Router()


class ISS:
    LED_RED = 3
    LED_GREEN = 5
    BUZZER = 29
    BUTTON = 31
    MOTION = 7
    SERVO = 11

    PASSED = False
    FAILED_TRIES = 0
    FAILED_TIMESTAMP = time.time()
    ALARM_MESSAGE = 'Object Security Violation!'
    ALARM_OFF_MESSAGE = 'Alarm off'

    led = LED(LED_RED, LED_GREEN)
    reader = SimpleMFRC522()

    def __init__(self):
        GPIO.setup(self.BUTTON, GPIO.IN)
        GPIO.setup(self.MOTION, GPIO.IN)
        GPIO.setup(self.BUZZER, GPIO.OUT, initial=0)
        GPIO.setup(self.SERVO, GPIO.OUT)
        self.servo = GPIO.PWM(11, 50)

        self.servo.start(7)

    def alarm(self):
        logger.warning(self.ALARM_MESSAGE)
        router.send_message(self.ALARM_MESSAGE)
        user, scaned = [None, None]
        while not all([user, scaned]):
            user, scaned = self.scan_rfid()
            signal_point(self.BUZZER)
        logger.info(self.ALARM_OFF_MESSAGE)
        router.send_message(self.ALARM_OFF_MESSAGE)
        self.FAILED_TRIES = 0
        time.sleep(1)
    
    def close_door(self):
        self.servo.ChangeDutyCycle(7)

    def open_door(self):
        self.servo.ChangeDutyCycle(11)
    
    def scan_rfid(self):
        uid = self.reader.read_no_block()
        scaned = False

        if all(uid):
            scaned = True
            uid = str(uid).replace("'", '"')
            logger.info(f'Scaned UID {uid}')
            
            with ps_client.connection.cursor() as cursor:
                user = ps_client.get_user_by_access_key(uid, cursor=cursor)
            
            return user, scaned
        return False, scaned
        

    def main(self):
        logger.info('Start ISS session')

        try:
            while True:
                self.led.turn_off_leds()

                user, scaned = self.scan_rfid()
                
                if scaned:            
                    if user:
                        logger.info(f'Access allowed for user {user.id}')
                        self.led.turn_green_on()
                        self.FAILED_TRIES = 0
                        if self.PASSED:
                            self.close_door()
                            self.led.turn_off_leds()
                            self.PASSED = False
                            logger.info(f'User {user.id} has left the object')
                        else:
                            self.open_door()
                            self.PASSED = True
                            logger.info(f'User {user.id} in object')
                    else:
                        self.FAILED_TRIES += 1
                        self.FAILED_TIMESTAMP = time.time()
                        if self.PASSED:
                            self.alarm()
                        else:
                            self.led.turn_red_on()
                            self.PASSED = False
                        if time.time() - self.FAILED_TIMESTAMP < 180 and self.FAILED_TRIES > 2:
                            self.alarm()
                    time.sleep(1.5)

                if time.time() - self.FAILED_TIMESTAMP > 180:
                    self.FAILED_TRIES = 0
# 
#                 if GPIO.input(self.MOTION) and not self.PASSED:
#                     self.alarm()
        except KeyboardInterrupt:
            GPIO.cleanup()
            logger.info('End ISS Session')


if __name__ == '__main__':
    ISS_object = ISS()
    ISS_object.main()
