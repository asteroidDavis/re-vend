#!/usr/bin/python
import sqlite3
import re
import sys

class Student:
    
    #the number of students who have used this program
    currentUsers = 0
    totalUsers = 0

    
    def __init__(self, studentNumber, RFIDCode, hasG2G, studentDatabase):
        
        #this could be tricked by calling del then init
        Student.totalUsers += 1
        
        #sets default studentNumber to 0
        self.studentNumber = studentNumber
        self.RFIDCode = RFIDCode
        self.hasG2G = hasG2G
        self.studentDataBase = studentDatabase
        
        #connects the student to our database
        self.studentConnection = sqlite3.connect(self.studentDataBase)
        self.studentCursor = self.studentConnection.cursor()
    
    def isNumber(self, idInput):
        try:
            float(idInput)
            return True
        except ValueError:
            return False

    def isInputStudentId(self, idInput):
        if(re.match(r'^[0-9]{9}?$', str(idInput))):
            return True
        else:
            return False

    def setStudentNumber(self, idInput):
        self.studentNumber = idInput

    def isInputRFID(self, idInput):
        if(re.match(r'^[0-9]{10}$', str(idInput))):
            return True
        else:
            return False

    def setRFIDCode(self, idInput):
        self.RFIDCode = idInput
        
    def isStudentInDB(self):
        
        if(self.isInputStudentId(self.studentNumber)):
            #checks if the student is already in the database
            self.studentConnection.execute(''' SELECT EXISTS(
                SELECT 1 FROM studentG2G WHERE
                Id=?)''', (self.studentNumber, )
            )
        elif(self.isInputRFID(self.RFIDCode)):
            self.studentConnection.execute(''' SELECT EXISTS(
                SELECT 1 FROM studentG2G WHERE
                RFID=?)''', (self.RFIDCode, )
            )

        if(self.studentCursor.fetchone()):
            return True
        else:
            return False

    def setHasG2GFromDB(self):
        if(self.isStudentInDB):
            self.studentCursor.execute('''SELECT Green2Go FROM studentG2G WHERE Id=?''',(self.studentNumber,))
            self.hasG2G = self.studentCursor.fetchone()
        else:
            self.hasG2G = False

    def setStudentNumberFromDB(self):
        if(self.isStudentInDB):
            self.studentCursor.execute('''SELECT Id FROM studentG2G WHERE RFID=?''', (self.RFIDCode,))
            self.studentNumber = self.studentCursor.fetchone()
        else:
            warnings.warn('Student RFID has no associated studentNumber')

    def setHasG2G(self, g2gStatus):
        self.hasG2G = g2gStatus
    
    def updateStudentDatabase(self):
        #create the student database if it's not created
        self.studentCursor.execute('''CREATE TABLE IF NOT EXISTS studentG2G(
            Id          INT PRIMARY KEY,
            RFID        INT,
            Green2Go    BOOLEAN
        )''')
        #adds a student
        self.studentConnection.execute('''
            INSERT INTO studentG2G (Id, RFID, Green2Go)
            VALUES (?, ?, ?)''', (self.studentNumber, self.RFIDCode, self.hasG2G.astype(int),)
        )
        #commits the update after each new student
        self.studentConnection.commit()
        
    def removeStudentFromDatabase(self):
        
        #removes this student from the database
        self.studentCursor.execute('''
            DELETE from studentG2G where Id = (?)''', (self.studentNumber,)
        )
        #commits the update after each student is removed
        self.studentConnection.commit()
        self.studentConnection.close()
