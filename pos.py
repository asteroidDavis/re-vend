#Point of Sale code By Nate Davis and Chris Schoener
#For now, simply scans a card and shows green light if server verifies
#We should have it play the sound effect from when sonic gets a ring

import ConfigParser 
import time
from light import *
from Student import *

def main():
    config = ConfigParser.RawConfigParser()
    config.read("posconfig.txt") 
    waitSecs = config.getint("general","seconds_lights_on")

    greenLight = light(config.getint("light", "greenPin"))
    redLight = light(config.getint("light", "redPin"))
    # ^ not worth reading ^

    greenLight.off()
    redLight.off()

    while 1:

        currentStudent = Student(0, 0, False, 'students.db')
 
        #process to allow id input in any order and validates the student does not have a G2G container
        idInput = raw_input('Scan RFID or student Id')
        greenLight.off()
        redLight.off()

        #student number first workflow
        if(currentStudent.isInputStudentId(idInput)):
            #sets studentNumber to scanned card
            currentStudent.setStudentNumber(idInput)
            #reads DB g2g bool
            currentStudent.setHasG2GFromDB()
            #student hasG2G
            if(currentStudent.hasG2G):
                #Red light
                redLight.on()
                greenLight.off()
            else:
                #scan RFID
                idInput = raw_input('Enter RFID')
                while(not(currentStudent.isInputRFID(idInput))):
                    redLight.on()
                    greenLight.on()
                currentStudent.setRFIDCode(idInput)
                currentStudent.setHasG2G(False)
                redLight.off()
                greenLight.on()
                currentStudent.updateStudentDatabase()
        #RFID first workflow
        elif(currentStudent.isInputRFID(idInput)):
            currentStudent.setRFIDCode(idInput)
            idInput=raw_input('Enter student Id')
            while(not(currentStudent.isInputStudentId(idInput))):
                redLight.on()
                greenLight.on()
            currentStudent.setStudentNumber(idInput)
            currentStudent.setHasG2GFromDB()
            if(currentStudent.hasG2G):
                greenLight.off()
                redLight.on()
            else:
                redLight.off()
                greenLight.on()
                currentStudent.setHasG2G(False)
                currentStudent.updateStudentDatabase()
        else:
            redLight.on()
            greenLight.on()
            
main()

