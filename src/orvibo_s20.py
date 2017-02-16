import time
#from S20control import orviboS20
from common import iniToDict, CONFIG_PATH
import os

settings = iniToDict(CONFIG_PATH)
failcount = 0
#power_socket = orviboS20()

def on():
    #power_socket.poweron(settings["beddit"]["relay_ip"], settings["beddit"]["relay_mac"])
    os.system("S20control poweron " + settings["beddit"]["relay_ip"] + " " + settings["beddit"]["relay_mac"])

def off():
    # power_socket.poweroff(settings["beddit"]["relay_ip"], settings["beddit"]["relay_mac"])
    os.system("S20control poweroff " + settings["beddit"]["relay_ip"] + " " + settings["beddit"]["relay_mac"])

def restart():
    off()
    time.sleep(3)
    on()
            
            

if __name__ == "__main__":
    restart()
