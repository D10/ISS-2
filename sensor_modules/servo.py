import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
servo1 = GPIO.PWM(11, 50)

servo1.start(7)
time.sleep(2)


def close_door():
    servo1.ChangeDutyCycle(7)


def open_door():
    servo1.ChangeDutyCycle(11)


if __name__ == '__main__':
    test_value = 0
    while test_value < 3:
        close_door()
        time.sleep(2)
        open_door()
        time.sleep(2)
        test_value += 1
        
    # servo1.stop()
