import RPi.GPIO as GPIO


class LED:
    
    def __init__(self, LED_RED, LED_GREEN):
        self.LED_RED = LED_RED
        self.LED_GREEN = LED_GREEN

    def turn_led_on(self, led):
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, GPIO.HIGH)

    def turn_led_off(self, led):
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, GPIO.LOW)
        
    def turn_off_leds(self):
        self.turn_led_off(self.LED_GREEN)
        self.turn_led_off(self.LED_RED)

    def turn_green_on(self):
        self.turn_led_off(self.LED_GREEN)
        self.turn_led_on(self.LED_RED)

    def turn_red_on(self):
        self.turn_led_off(self.LED_RED)
        self.turn_led_on(self.LED_GREEN)
