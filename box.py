#By Chris Schoener and Nate Davis, Python 2

#Keyboard buffer doesn't work over SSH!!!

#TODO: 1) report tray to EC2 and receive response
#      2) add proper values to cfg (motor steps, light ports) and test

import ConfigParser #uses built in module to read config
import ast # for lists in config
from evdev import InputDevice, categorize, ecodes
from select import select
import argparse
import sys
from solenoid import *
import time
from light import *
from Student import *


    
#def reportTray(Tray)
#fake for now
#I'm thinking we set EC2 to a static IP and open a port, then send packets
#EC2 then just sends a 1 or 0 back to the IP it received from
#The question is what sort of communication does the PSU network allow
#Server will almost always return 1 unless someone manages to scan a non-box rfid
#    return 1


def main():
    config = ConfigParser.RawConfigParser()
    config.read("/opt/re-vend/boxconfig.txt") 
    waitSecs = config.getint("general","seconds_box_is_unlocked")
    lock = solenoid(config.getint("lock", "pin"), waitSecs)
    greenLight = light(config.getint("light", "greenPin"))
    redLight = light(config.getint("light", "redPin"))
    # ^ not worth reading ^

    scancodes = {
        0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
        10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
        20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
        30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
        40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
        50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
    }
    #sets up the RFID keyboard event
    keyboards = getKeyboards()
    rfidKeyboard = InputDevice(keyboards)

    #reads a keyboard event
    print("Scan an rfid tag")

    greenLight.off()
    redLight.off()
    
    while rfidKeyboard:

        currentStudent = Student(0, 0, False, 'students.db')
        idInput = ''
        
        for rfidEvent in rfidKeyboard.read_loop():
            if rfidEvent.type == ecodes.EV_KEY:
                data = categorize(rfidEvent)
                if(data.keystate == 1):
                    key_lookup = scancodes.get(data.scancode) or u'UNKOWN:{}'.format(data.scancode)
                    if(key_lookup.isdigit()):
                        idInput += format(key_lookup)

            if(len(idInput) == 10):
                break

        print("idInput is %d" %int(idInput))
 
        #checks if the user is scanning one of our rfid tags
        if(currentStudent.isInputRFID(idInput)): #report tray and open box
            #checks if the student has ever used one of our rfid tags
            if(currentStudent.isStudentInDB()):
                self.setStudentNumberFromDB()
                self.setHasG2GFromDB()
                #checks if the student had taken out a G2G box
                if(self.hasG2G):
                    redLight.off()
                    greenLight.on()
                    lock.unlockThenLock()
                else:
                    redLight.on()
                    greenLight.off()
            else:
                redLight.on()
                greenLight.off()
        else:
            redLight.on()
            greenLight.on()

        #gets new input from the rfid scanner
        print("Scan an rfid tag")       

#gets the keyboard file passed as the only argument to this script
def getKeyboards():
    #tries to use the keyboard option
    parser = argparse.ArgumentParser(description='Use a keyboard to add change a students status in a remote database')
    parser.add_argument('-k', '--keyboard')
    args = parser.parse_args()
    return args.keyboard

main()
    
