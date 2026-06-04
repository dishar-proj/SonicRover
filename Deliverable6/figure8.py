import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motors
motor1_in1 = 20
motor1_in2 = 21
motor2_in1 = 18
motor2_in2 = 19
enable_motor1 = 13  # Enable pin 1
enable_motor2 = 12  # Enable pin 2

# Set up the motor control pins
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

# Move forward for a given time
def move_forward(time_to_move):
    control_motor(1, 1, 100, 77.5)  # Move both motors forward
    time.sleep(time_to_move + 0.6)
    control_motor(0, 0, 0, 0)  # Stop motors
    time.sleep(1)

# Make a left turn (~120 degrees for a curved path)
def turn_left():
    control_motor(1, 1, 40, 100)  # Motor 1 slower, Motor 2 forward
    time.sleep(3.1)  # Adjust this time for a smoother left turn
    control_motor(0, 0, 0, 0)  # Stop motors
    time.sleep(1)

# Make a right turn (~120 degrees for a curved path)
def turn_right():
    control_motor(1, 1, 100, 30)  # Motor 1 forward, Motor 2 slower
    time.sleep(3.9)  # Adjust this time for a smoother right turn
    control_motor(0, 0, 0, 0)  # Stop motors
    time.sleep(1)

# Function to calculate the time to move 3 feet
def move_distance(distance):
    wheel_diameter = 0.062  
    wheel_circumference = 3.1416 * wheel_diameter  
    motor1_rpm = 135  
    motor2_rpm = 126  

    meters_per_minute1 = (motor1_rpm * wheel_circumference) / 60  
    meters_per_minute2 = (motor2_rpm * wheel_circumference) / 60  

    distance_meters = distance * 0.3048  
    time_to_move = distance_meters / min(meters_per_minute1, meters_per_minute2)  

    #print(f"Time to move {distance} feet: {time_to_move + 0.6} seconds")
    
    move_forward(time_to_move)

# Move in a figure-8 pattern twice
def move_figure_8_twice(): 
        move_distance(3.3)  # Move forward 3 feet
        turn_right()  # Turn left
        move_distance(3.2)  # Move forward 3 feet
        turn_left()  # Turn right
        move_distance(3.3)  # Move forward 3 feet
        turn_right()  # Turn right
        move_distance(3.2)  # Move forward 3 feet
        turn_left()  # Turn left

# Main loop
try:
    time.sleep(3)
    GPIO.output(20, GPIO.HIGH)  # LED ON
    move_figure_8_twice()  # Move in a figure-8 pattern twice
finally:
    pwm_motor1.stop()
    pwm_motor2.stop()
    GPIO.cleanup() # Clean up the GPIO pins
