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
import re

def main():
    config = ConfigParser.RawConfigParser()
    config.read("posconfig.txt") 
    waitSecs = config.getint("general","seconds_lights_on")
    
    #sets up the socket
    host = config.get("database", "host")
    port = config.getint("database", "port")
    responseSize = config.getint("database","responseSize") 
    
    greenLight = light(config.getint("light", "greenPin"))
    redLight = light(config.getint("light", "redPin"))
   
    (rfidKeyboard, magneticKeyboard) = getKeyboards()  
    
    greenLight.off()
    redLight.off() 
    
    #print("Connecting to ", host)
    #posSocket.connect((host, port))


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
        
            print("Connecting to ", host)
            posSocket = socket.socket()
            posSocket.connect((host, port))

            currentStudent.setHasG2G(reportId(idInput,posSocket, host, port, responseSize))
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
                reportRfid(idInput, posSocket, host, port)
        #RFID first workflow
        elif(currentStudent.isInputRFID(idInput)):
            currentStudent.setRFIDCode(idInput)
            idInput=readKeyboards(rfidKeyboard, magneticKeyboard)
            while(not(currentStudent.isInputStudentId(idInput))):
                redLight.on()
                greenLight.on()
                idInput = readKeyboards(rfidKeyboard, magneticKeyboard)

            print("Connecting to ", host)
            posSocket = socket.socket()
            posSocket.connect((host, port))

            currentStudent.setStudentNumber(idInput)
            currentStudent.setHasG2G(reportId(idInput, posSocket, host, port, responseSize))
            if(currentStudent.hasG2G):
                greenLight.off()
                redLight.on()
            else:
                redLight.off()
                greenLight.on()
                reportRfid(currentStudent.RFIDCode,posSocket, host, port)
        else:
            redLight.on()
            greenLight.on()
        print("closing connection with", host)
        posSocket.close()

def reportRfid(rfid, posSocket, host, port):
    sent = posSocket.send(rfid)
    if(sent == 0):
        raise RuntimeError("socket connection broken")

def reportId(studentId, posSocket, host, port, responseSize):
    sent = posSocket.send(studentId)
    if(sent == 0):
        raise RuntimeError("socket connection broken")
    #expecting an integer reply 1 means student is ok 0 means student is not ok 
    posResponse = struct.unpack('<I', posSocket.recv(8))
    print("recieved ", posResponse)
    if(posResponse[0] == 0):
        print("student has no g2g containter")
        return False
    else:
        print("student already has g2g containter")
        return True

def getKeyboards():
    #tries to use the keyboard option
    parser = argparse.ArgumentParser(description='Use a keyboard to add change a students status in a remote database')
    parser.add_argument('--rfidKeyboard')
    parser.add_argument('--magneticKeyboard')
    args = parser.parse_args()
    return (args.rfidKeyboard, args.magneticKeyboard)

def readKeyboards(rfidKeyboard, magneticKeyboard):

    scancodes = {
        0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
        10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
        20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
        30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
        40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
        50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT' 
    }


    idInput = '';

    devices = map(InputDevice, (rfidKeyboard, magneticKeyboard))
    devices = {dev.fd: dev for dev in devices}
    print("Scan rfid or studentId")    

    while devices:
        r,w,x = select(devices, [], [])
        for fd in r:
            for event in devices[fd].read():
                if(event.type == ecodes.EV_KEY):
                    data = categorize(event)
                    if(data.keystate == 1):
                        key_lookup = scancodes.get(data.scancode)
                        if(key_lookup == 'CRLF'):
                            print("Keyboar entered: ", idInput)
                            return str(idInput)
                        elif(key_lookup == None):  
                            print("Keyboard entered: ", idInput)
                            magCapture = re.search(r'A([0-9]{9})=', idInput)
                            idInput = magCapture.group(1)
                            print("Captured ", idInput)
                            return str(idInput)
                        else:
                            idInput += format(key_lookup)

main()

