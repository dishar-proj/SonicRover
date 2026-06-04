# import statements
import RPi.GPIO as GPIO
import time
import machine

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor Pins
motor1_in1 = 20
motor1_in2 = 21
motor2_in1 = 18
motor2_in2 = 19
enable_motor1 = 13  # Enable pin 1
enable_motor2 = 12  # Enable pin 2

# Bump Switch
bump_switch_pin = 23  # Bump switch pin (adjust as needed)

# Bump Switch Set up
GPIO.setup(bump_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up motor control pins as output
GPIO.setup(motor1_in1, GPIO.OUT)
GPIO.setup(motor1_in2, GPIO.OUT)
GPIO.setup(motor2_in1, GPIO.OUT)
GPIO.setup(motor2_in2, GPIO.OUT)
GPIO.setup(enable_motor1, GPIO.OUT)
GPIO.setup(enable_motor2, GPIO.OUT)

# PWM Setup
pwm_motor1 = GPIO.PWM(enable_motor1, 100)
pwm_motor2 = GPIO.PWM(enable_motor2, 100)
pwm_motor1.start(0)
pwm_motor2.start(0)

# Function to control motors (direction and speed)
def control_motor(direction_motor1, direction_motor2, speed_motor1, speed_motor2):
    GPIO.output(motor1_in1, GPIO.HIGH if direction_motor1 == 1 else GPIO.LOW)
    GPIO.output(motor1_in2, GPIO.LOW if direction_motor1 == 1 else GPIO.HIGH)
    GPIO.output(motor2_in1, GPIO.HIGH if direction_motor2 == 1 else GPIO.LOW)
    GPIO.output(motor2_in2, GPIO.LOW if direction_motor2 == 1 else GPIO.HIGH)
    pwm_motor1.ChangeDutyCycle(speed_motor1)
    pwm_motor2.ChangeDutyCycle(speed_motor2)

# Read bump switch state
def is_bump_switch_pressed():
    return GPIO.input(bump_switch_pin) == GPIO.LOW  # LOW when pressed

# Move forward for a given time
def move_forward(time_to_move):
    control_motor(1, 1, 100, 77.5)  # Move both motors forward
    time.sleep(time_to_move + 0.8)
    control_motor(0, 0, 0, 0)  # Stop motors
    time.sleep(0.1)

#main loop
max_distance = 5.2  # Maximum distance in feet
        while True:
            move_forward(max_distance)  # Move forward for the calculated time (max 5.2 feet)
            if is_bump_switch_pressed():
                print("Bump switch activated! Stopping.")
                control_motor(0, 0, 0, 0)  # Stop the car immediately
                break
