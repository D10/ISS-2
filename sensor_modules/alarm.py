import time

import RPi.GPIO as GPIO

BUZZER = 21
ALARM_TIME = 0.5


def signal_point(port):
    GPIO.output(port, GPIO.HIGH)
    time.sleep(ALARM_TIME)
    GPIO.output(port, GPIO.LOW)
    time.sleep(ALARM_TIME)


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER, GPIO.OUT)
    try:
        while True:
            alarm(BUZZER)
    except KeyboardInterrupt:
        print('Quit')
        GPIO.cleanup()
