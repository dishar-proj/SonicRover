import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor Pins
motor1_in1 = 20
motor1_in2 = 7
motor2_in1 = 18
motor2_in2 = 19
enable_motor1 = 13  # Enable pin 1
enable_motor2 = 12  # Enable pin 2

# ADC
comp1_output = 24 # MSB
comp2_output = 25  # Middle bit
comp3_output = 8  # LSB

# Bump Switch
bump_switch_pin = 23  # Bump switch pin (adjust as needed)

# Filter Control Pins
filter_C8 = 5
filter_C6 = 6
GPIO.setup(filter_C8, GPIO.OUT)
GPIO.setup(filter_C6, GPIO.OUT)
GPIO.output(filter_C8, GPIO.LOW)
GPIO.output(filter_C6, GPIO.LOW)

# Set up comparator output pins as input
GPIO.setup(comp1_output, GPIO.IN)
GPIO.setup(comp2_output, GPIO.IN)
GPIO.setup(comp3_output, GPIO.IN)

# Bump Switch Set up
GPIO.setup(bump_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up DIP switch pins as input
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)

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

# Motor control function
def control_motor(direction_motor1, direction_motor2, speed_motor1, speed_motor2):
    GPIO.output(motor1_in1, GPIO.HIGH if direction_motor1 == 1 else GPIO.LOW)
    GPIO.output(motor1_in2, GPIO.LOW if direction_motor1 == 1 else GPIO.HIGH)
    GPIO.output(motor2_in1, GPIO.HIGH if direction_motor2 == 1 else GPIO.LOW)
    GPIO.output(motor2_in2, GPIO.LOW if direction_motor2 == 1 else GPIO.HIGH)
    pwm_motor1.ChangeDutyCycle(speed_motor1)
    pwm_motor2.ChangeDutyCycle(speed_motor2)

try:
    print("Moving forward...")
    control_motor(1, 1, 100, 90)  # Forward
    time.sleep(2)

    print("Moving backward...")
    control_motor(0, 0, 100, 90)  # Backward
    time.sleep(2)

    print("Stopping.")
    control_motor(0, 0, 0, 0)  # Stop

finally:
    pwm_motor1.stop()
    pwm_motor2.stop()
    GPIO.cleanup()