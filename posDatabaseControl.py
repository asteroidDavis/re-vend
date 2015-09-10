#!/usr/bin/python
import socket
import struct
from Student import *

def main():
    #sets up the socket
    studentSocket = socket.socket()
    host = socket.gethostname()
    port = 3307
    studentSocket.bind((host, port))

    #max 5 pending connections
    studentSocket.listen(5)

    #as long as a socket exists
    while studentSocket:

        #creates an empty student for each new connection
        currentStudent = Student(0, 0, False, 'students.db')
         
        print("waiting for a connection")
        connection, address = studentSocket.accept()
        print("Connection from", address)
        #we're expecting a studentID value to be 9 characters
        studentId = connection.recv(9)
        print("Got: ", studentId)
        (response, currentStudent) = checkStudentId(studentId, currentStudent)
        print("Sending", response)
        connection.send(struct.pack('<I', response))
        if(response == 0):
            #recieves the rfid value
            studentRFID = connection.recv(10)
            print("Got: ", studentRFID)
            addRfid(studentRFID, currentStudent)
        print("Closing connection")
        connection.close()

def checkStudentId(idInput, currentStudent):
    if(currentStudent.isInputStudentId(idInput)):
        currentStudent.setStudentNumber(idInput)
        currentStudent.setHasG2GFromDB()
        if(currentStudent.hasG2G):
            print("Student already has G2G")
            return (1, currentStudent)
        else:
            print("Student does not have G2G")
            return (0, currentStudent)
    else:
        print("Unrecognized input")
        return (1, currentStudent)

#performs the correct update based on the recieved RFID code
def addRfid(idInput, currentStudent):
    #first checks if a reset code has been scanned
    if(isRfidInputReset(idInput)):
        #marks the student as not having an rfid 
        currentStudent.resetHasG2G()
    else:
        #sets the students recieved values
        currentStudent.setRFIDCode(idInput)
        currentStudent.setHasG2G(1)
        #updates the DB
        currentStudent.updateStudentDatabase()

#checks the RFID input for a reset code
def isRfidInputReset(RfidInput):
    return (RfidInput == '0123456789')

main()
