#!/usr/bin/python
#By Chris Schoener and Nate Davis, Python 2.7

import ConfigParser #uses built in module to read config
from evdev import InputDevice, categorize, ecodes
from select import select
import struct
import argparse
import sys
from solenoid import *
import time
import socket
from Student import *

    
def reportTray(rfid, boxSocket, host, port):
    sent = boxSocket.send(rfid)
    if(sent == 0):
        raise RuntimeError("socket connection broken")
    #returns 1 on success
    else: 
        return 1

def main():
    #sets up the box config parser
    config = ConfigParser.RawConfigParser()
    config.read("/opt/re-vend/boxconfig.txt") 
 
    #sets up the socket information
    host = config.get("database", "host")
    port = config.getint("database", "port")   

    #sets up the solenoid
    waitSecs = config.getint("general","seconds_box_is_unlocked")
    lock = solenoid(config.getint("lock", "pin"), waitSecs)

    #ascii table for readin keyboard events
    scancodes = {
        0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
        10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
        20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
        30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
        40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
        50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
    }
    #gets the keyboard file from the parameters
    keyboards = getKeyboards()
    #marks the keyboard as input
    rfidKeyboard = InputDevice(keyboards)

    #reads a keyboard event
    print("Scan an rfid tag")

    #ensures there is an input device
    while rfidKeyboard:

        #empties the student and the idInput
        currentStudent = Student(0, 0, False, 'students.db')
        idInput = ''
        
        #listens to every keypress
        for rfidEvent in rfidKeyboard.read_loop():
            #makes sure the keyboard is sending a key
            if rfidEvent.type == ecodes.EV_KEY:
                rfidData = categorize(rfidEvent)
                #makes sure the key is pressed
                if(rfidData.keystate == 1):
                    #looks up the key from the scancode table
                    key_lookup = scancodes.get(rfidData.scancode) or u'UNKOWN:{}'.format(data.scancode)
                    #rfid only uses numbers
                    if(key_lookup.isdigit()):
                        #puts any pressed number into the rfid input
                        idInput += format(key_lookup)
            #our rfid tags are 10 numbers so stop listening to input once there are 10 numbers
            if(len(idInput) == 10):
                break

        print("idInput is %d" %int(idInput))
        print("Connecting to %s:%s " %(host, port))
        #sets up the socket
        boxSocket = socket.socket()
        boxSocket.connect((host, port)) 

        #checks if the user is scanning one of our rfid tags
        if(currentStudent.isInputRFID(idInput)): 
            print("RFID scanned. Unlocking box")
            lock.unlockThenLock()
            if(reportTray(idInput, boxSocket, host, port)):
                print("RFID accepted")
            else:
                print("RFID rejected")
        else:
            print("Invalid input")

        boxSocket.close()
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
    
