from Student import *
from stepperMotor import *
from array import array
import time

#def main():
#    
#    testStudent = Student(0, 'a', False, 'students.db')
#    testStudent.readInput()
 
def main():
    coilPins=[4, 17, 23, 24]
    testMotor = stepperMotor(128, 128, 0.0025, coilPins) 
    print "Got to moveMotor(1)\n"
    testMotor.moveMotor(1)
    time.sleep(5)
    testMotor.moveMotor(-1) 
   
main()
print('Test Over')

exit()
