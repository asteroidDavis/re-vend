#Point of Sale code By Nate Davis and Chris Schoener
#For now, simply scans a card and shows green light if server verifies
#We should have it play the sound effect from when sonic gets a ring

import ConfigParser 
import time
import light

def testID(id)
#same problems as stated in box.py
    return 1 # for now
    

def main()
    config = ConfigParser.RawConfigParser()
    config.read("boxconfig.txt") 
    waitSecs = config.getint("general","seconds_lights_on")
    greenLight = light(config.getint("light", "greenPin"))
    redLight = light(config.getint("light", "redPin"))
    # ^ not worth reading ^

    while 1:
        greenLight.off()
        redLight.on()
        id = raw_input()
        if (testID(id) == 1):
            greenLight.on()
            redLight.off()
            time.sleep(5)
            

            
            
main()