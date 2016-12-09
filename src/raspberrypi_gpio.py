import RPi.GPIO as GPIO
import time

ON_PIN = 23
OFF_PIN = 24

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)
# set up GPIO output channel
GPIO.setup(ON_PIN, GPIO.OUT)
GPIO.setup(OFF_PIN, GPIO.OUT)


def switch(pin):
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin,GPIO.LOW)

def on():
    switch(ON_PIN)

def off():
    switch(OFF_PIN)

def restart():
    off()
    time.sleep(2)
    on()

if __name__ == "__main__":
    restart()
