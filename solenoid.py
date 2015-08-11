#!/usr/bin/python
import RPi.GPIO as GPIO
import time

class solenoid:

    #sets up a solenoid object
    #parameters:
    #   lockPin: The GPIO pin controlling the lock
    #   unlockTime: The delay between unlocking and locking in seconds
    def __init__(self, lockPin, unlockTime):
        GPIO.setmode(GPIO.BCM)

        self.lockPin = lockPin
        self.unlockTime = unlockTime
        
        self.setupGPIO()

    def setupGPIO(self):
        GPIO.setup(self.lockPin, GPIO.OUT)

    #extends the solenoid by removing power
    def lock(self):
        GPIO.output(self.lockPin, 0)

    #unlocks the solenoid by running current throug it
    def unlock(self):
        GPIO.output(self.lockPin, 1)

    #unlocks for the unlockTime
    def unlockThenLock(self):
        self.unlock()
        time.sleep(self.unlockTime)
        self.lock()

