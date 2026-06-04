import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2, GPIO.OUT)
GPIO.output(2, GPIO.LOW)

#array with GPIOs in order from left to right, top row to bottom row
array = [2, 14, 18, 23, 9, 8, 12, 16, 21, 3, 15, 27,24, 25, 7, 5, 13, 26, 4, 17, 22, 10, 11, 6, 19, 20]

for gpio in array:
  GPIO.setup(gpio, GPIO.OUT)
  #time.sleep(0.5)
  GPIO.output(gpio, 0) #intially turn off the light
  time.sleep(0.5)
  print("LED ON") #debugging
  GPIO.output(gpio, 1) #turn LED on
  time.sleep(0.5)
  print("LED off") #debugging 
  GPIO.output(gpio, 0) #turn LED off
