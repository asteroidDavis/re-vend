#Point of Sale code By Nate Davis and Chris Schoener
#For now, simply scans a card and shows green light if server verifies
#We should have it play the sound effect from when sonic gets a ring

from evdev import InputDevice, categorize, ecodes
from select import select
import argparse
import sys
import struct
import socket
import ConfigParser 
import time
from light import *
from Student import *

def main():
    config = ConfigParser.RawConfigParser()
    config.read("posconfig.txt") 
    waitSecs = config.getint("general","seconds_lights_on")
    
    #sets up the socket
    boxSocket = socket.socket()
    host = config.get("database", "host")
    port = config.getint("database", "port")
    responseSize = config.getint("database","responseSize") 

    greenLight = light(config.getint("light", "greenPin"))
    redLight = light(config.getint("light", "redPin"))
   
    (rfidKeyboard, magneticKeyboard) = getKeyboards() 
    rfidKeyboard = InputDevice(rfidKeyboard)
    magneticKeyboard = InputDevice(magneticKeyboard) 
    
    greenLight.off()
    redLight.off()

    while rfidKeyboard and magneticKeyboard:
        
        idInput = readKeyboards(rfidKeyboard, magneticKeyboard)            

        currentStudent = Student(0, 0, False, 'students.db')
 
        #process to allow id input in any order and validates the student does not have a G2G container
        greenLight.off()
        redLight.off()

        #student number first workflow
        if(currentStudent.isInputStudentId(idInput)):
            #sets studentNumber to scanned card
            currentStudent.setStudentNumber(idInput)
            currentStudent.setHasG2G(reportId(idInput, host, port, responseSize))
            if(currentStudent.hasG2G):
                #Red light
                redLight.on()
                greenLight.off()
            else:
                #scan RFID
                idInput = readKeyboards(rfidKeyboard, magneticKeyboard)
                while(not(currentStudent.isInputRFID(idInput))):
                    redLight.on()
                    greenLight.on()
                    idInput = readKeyboards(rfidKeyboard, magneticKeyboard)
                redLight.off()
                greenLight.on()
                reportRfid(idInput, host, port, responseSize)
        #RFID first workflow
        elif(currentStudent.isInputRFID(idInput)):
            currentStudent.setRFIDCode(idInput)
            idInput=readKeyboards(rfidKeyboard, magneticKeyboard)
            while(not(currentStudent.isInputStudentId(idInput))):
                redLight.on()
                greenLight.on()
                idInput = readKeyboards(rfidKeyboard, magneticKeyboard)
            currentStudent.setStudentNumber(idInput)
            currentStudent.setHasG2G(reportId(idInput, host, port, responseSize))
            if(currentStudent.hasG2G):
                greenLight.off()
                redLight.on()
            else:
                redLight.off()
                greenLight.on()
                reportRfid(currentStudent.RFIDCode, host, port)
                currentStudent.updateStudentDatabase()
        else:
            redLight.on()
            greenLight.on()

def reportRfid(rfid, posSocket, host, port):
    posSocket.connect((host, port))
    sent = posSocket.send(rfid)
    if(sent == 0):
        raise RuntimeError("socket connection broken")
    posSocket.close()

def reportId(studentId, socket, host, port, responseSize):
    posSocket = socket
    posSocket.connect((host, port))
    sent = posSocket.send(studentId)
    if(sent == 0):
        raise RuntimeError("socket connection broken")
    #expecting an integer reply 1 means student is ok 0 means student is not ok 
    posResponse = struct.unpack('<I', posSocket.recv(8))
    posSocket.close()
    if(posResponse == 1):
        print("student has no g2g containter")
        return True
    else:
        print("student already has g2g containter")
        return False

def getKeyboards():
    #tries to use the keyboard option
    parser = argparse.ArgumentParser(description='Use a keyboard to add change a students status in a remote database')
    parser.add_argument('--rfidKeyboard')
    parser.add_argument('--magneticKeyboard')
    args = parser.parse_args()
    return (args.rfidKeyboard, args.magneticKeyboard)

def readKeyboards(rfidKeyboard, magneticKeyoard):

    scancodes = {
        0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
        10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
        20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
        30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
        40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
        50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
    }


    idInput = '';
    for rfidEvent in rfidKeyboard.read_loop():
        if(rfidEvent.type == ecodes.EV_KEY):
            rfidData = categorize(rfidEvent)
            if(rfidData.keystate == 1):
                key_lookup = scancodes.get(rfidData.scancode)
                if(key_lookup.isdigit()):
                    idInput += format(key_lookup)
        if(len(idInput) == 10):
            return idInput
        
    for magneticKeyboard in magneticKeyboard.read_loop():
        if(magneticEvent.type == ecodes.EV_KEY):
            magneticData = categorize(magneticEvent)
            if(magneticData.keystate == 1):
                key_lookup = scancodes.get(magneticData.scancode)
                if(key_lookup.isdigit()):
                    idInput += format(key_lookup)
        if(len(idInput) == 28):
            return idInput

               
main()

