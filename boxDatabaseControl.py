#!/usr/bin/python
import socket
import struct
from Student import *

def main():
    #sets up the socket
    studentSocket = socket.socket()
    host = socket.gethostname()
    port = 3306
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
        #we're expecting an rfid value to be one 8 byte integer
        studentData = connection.recv(10)
        studentRFID = int(studentData)
        print("Got: ", studentRFID)
        response = checkStudent(studentRFID, currentStudent)
        print("Closing connection")
        connection.close()

def checkStudent(idInput, currentStudent):
    if(currentStudent.isInputRFID(idInput)):
        currentStudent.setRFIDCode(idInput)
        if(currentStudent.isStudentInDB()):
            currentStudent.setStudentNumberFromDB()
            currentStudent.setHasG2GFromDB()
            if(currentStudent.hasG2G):
                currentStudent.setHasG2G(False)
                print("Marked student as not having G2G")
                return 1
            else:
                print("ERROR: Student marked as not G2G but RFID is tracked")
        else:
            print("Unrecognized RFID value")
    else:
        print("Unrecognized input")
    return 0

main()
