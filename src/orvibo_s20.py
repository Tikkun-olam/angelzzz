import time
from S20control import orviboS20
from common import iniToDict, CONFIG_PATH

settings = iniToDict(CONFIG_PATH)

def on():
    power_socket = orviboS20()
    power_socket.poweron(settings["beddit"]["relay_ip"], settings["beddit"]["relay_mac"])

def off():
    power_socket = orviboS20()
    power_socket.poweroff(settings["beddit"]["relay_ip"], settings["beddit"]["relay_mac"])

def restart():
    off()
    time.sleep(2)
    on()

if __name__ == "__main__":
    restart()
