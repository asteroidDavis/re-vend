include RPi.GPIO as GPIO
class light: #light can be set on or off, pin defined in cfg
    def __init__(self, pin)
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
    def on(self)
        GPIO.output(self.pin, 1)
    def off(self)
        GPIO.output(self.pin, 0)