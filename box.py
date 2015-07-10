#By Chris Schoener and Nate Davis, Python 2

#Keyboard buffer doesn't work over SSH!!!

#TODO: 1) report tray to EC2 and receive response
#      2) add proper values to cfg (motor steps, light ports) and test

import ConfigParser #uses built in module to read config
import ast # for lists in config
import stepperMotor
import time
import light
    

    
def reportTray(Tray)
#fake for now
#I'm thinking we set EC2 to a static IP and open a port, then send packets
#EC2 then just sends a 1 or 0 back to the IP it received from
#The question is what sort of communication does the PSU network allow
#Server will almost always return 1 unless someone manages to scan a non-box rfid
    return 1


def main() 
    config = ConfigParser.RawConfigParser()
    config.read("boxconfig.txt") 
    waitSecs = config.getint("general","seconds_box_is_unlocked")
    motor = stepperMotor.stepperMotor(config.getint("motor","forwardSteps"), config.getint("motor","backwardsSteps") , config.getfloat("motor","delay"), ast.literal_eval(config.get("motor","coilPins")))
    greenLight = light(config.getint("light", "greenPin"))
    redLight = light(config.getint("light", "redPin"))
    # ^ not worth reading ^
    
    while 1:
        greenLight.off()
        redLight.on()
        
        Tray = raw_input() 
        if (reportTray(tray) == 1): #report tray and open box
            redLight.off()
            greenLight.on()
            motor.forward()
            time.sleep(waitSecs)
            motor.backwards()
            
main()
    