import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings (False)

#set up GPIO pins as input pins
GPIO.setup(4, GPIO.IN) #Bit3
GPIO.setup(17, GPIO.IN) #Bit2
GPIO.setup(27, GPIO.IN) #Bit1
GPIO.setup(22, GPIO.IN) #Bit0

#configure the GPIO pins for the LEDs as output pins/voltage pins
GPIO.setup(14, GPIO.OUT)#Bit3 LED (Red)
GPIO.setup(24, GPIO.OUT) #Bit2 LED (Yellow) 
GPIO.setup(25, GPIO.OUT) #Bit1 LED (Blue)
GPIO.setup(23, GPIO.OUT) #Bit0 LED (Green)

#Checking coniditions
loop = True
while loop==True:
    GPIO.setmode(GPIO.BCM)
    if (GPIO.input(4) == True) and (GPIO.input(17) == True) and (GPIO.input(27) == True) and (GPIO.input(22) == True): #Debug
        print("read 1111")
        GPIO.output(14, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(25, GPIO.HIGH)
        GPIO.output(23, GPIO.HIGH)
    elif (GPIO.input(4) == True) and (GPIO.input(17) == True) and (GPIO.input(27) == True) and (GPIO.input(22) == False): #Square
        print("read 1110")
        GPIO.output(14, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(25, GPIO.HIGH)
        GPIO.output(23, GPIO.LOW)
    elif (GPIO.input(4) == True) and (GPIO.input(17) == True) and (GPIO.input(27) == False) and (GPIO.input(22) == True): #Figure8
        print("read 1101")
        GPIO.output(14, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(25, GPIO.LOW)
        GPIO.output(23, GPIO.HIGH) 
    elif (GPIO.input(4) == True) and (GPIO.input(17) == True) and (GPIO.input(27) == False) and (GPIO.input(22) == False): #Straight
        print("read 1100")
        GPIO.output(14, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(25, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
    elif (GPIO.input(4) == True) and (GPIO.input(17) == False) and (GPIO.input(27) == True) and (GPIO.input(22) == True):
        print("read 1011")
        GPIO.output(14, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(25, GPIO.HIGH)
        GPIO.output(23, GPIO.HIGH)
        
    elif (GPIO.input(4) == True) and (GPIO.input(17) == False) and (GPIO.input(27) == True) and (GPIO.input(22) == False):
        print("read 1010")
        GPIO.output(14, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(25, GPIO.HIGH)
        GPIO.output(23, GPIO.LOW)
        
    elif (GPIO.input(4) == True) and (GPIO.input(17) == False) and (GPIO.input(27) == False) and (GPIO.input(22) == True): #Multiple
        print("read 1001")
        GPIO.output(14, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
        GPIO.output(23, GPIO.HIGH)
    elif (GPIO.input(4) == True) and (GPIO.input(17) == False) and (GPIO.input(27) == False) and (GPIO.input(22) == False): #Single
        print("read 1000")
        GPIO.output(14, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
    else: #Don't move
        print("bit 4 is 0")
        GPIO.output(14, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
