#Written  By: Nathan Davis
import RPi.GPIO as GPIO
import time

class stepperMotor:
 
    #constructor
    def __init__(self, frontSteps, backSteps, delay, coilPins, enablePin = 16):
        self.setupGPIO(enablePin, coilPins)
        #the number of steps to move dispensing one carabiner
        self.frontSteps = frontSteps
        #the number of steps to move to reset the position
        self.backSteps = backSteps
        #the delay between each step in seconds (5ms is smooth with no resistance)
        self.delay = delay
                
    def setupGPIO(self, enablePin, coilPins):
        #sets the numbering system for GPIO pins
        GPIO.setmode(GPIO.BCM)
        #sets GPIO pin numbers
        #I could turn these into variables for using multiple motors on one driver
        self.enable_pin = enablePin
        self.coil_A_1_pin = coilPins[0]
        self.coil_A_2_pin = coilPins[1]
        self.coil_B_1_pin = coilPins[2]
        self.coil_B_2_pin = coilPins[3]
        #sets up the pins
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)  
        GPIO.output(self.enable_pin, 1)
    
    def moveMotor(self, direction):
        #-1 counter-clockwise, 0 stationary, 1 clockwise
        self.direction = direction
        if (self.direction > 0):
            self.forward()
            self.endStepping()
        elif (self.direction < 0):
            self.backwards()
            self.endStepping()
        else:
            self.endStepping()
 
    def forward(self):  
        for i in range(0, self.frontSteps):
            self.setStep(1, 0, 1, 0)
            time.sleep(self.delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(self.delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(self.delay)
            self.setStep(1, 0, 0, 1)
            time.sleep(self.delay)
     
    def backwards(self):  
        for i in range(0, self.backSteps):
            self.setStep(1, 0, 0, 1)
            time.sleep(self.delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(self.delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(self.delay)
            self.setStep(1, 0, 1, 0)
            time.sleep(self.delay)
     
      
    def setStep(self, w1, w2, w3, w4):
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)
      
    def endStepping(self):
        self.setStep(0, 0, 0, 0)
 
