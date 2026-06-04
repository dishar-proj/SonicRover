# Simple One
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# setting up pin 17 as the 3.3V source
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)

# set GPIO pins for LED and button switch
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)
GPIO.setup(25, GPIO.IN)


while True:
    if GPIO.input(25):
        GPIO.output(18, False)
    else:
        GPIO.output(18, True)
        
