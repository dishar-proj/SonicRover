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

# Configure GPIO pins for LEDs
GPIO.setup(20, GPIO.OUT)  # LED for straight

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

# Transfer function constants (as before)
K1 = 41.044 
K2 = 42.24  
tau = 0.000125  
dt = 0.1  

rpm_motor1 = 0
rpm_motor2 = 0

# Motor speed update using the transfer function (as before)
def update_motor_speed(voltage, motor_num):
    if motor_num == 1:
        K = K1
    else:
        K = K2
    motor_speed = (K / tau) * voltage * dt + rpm_motor1
    return motor_speed

# Control motors (direction and speed)
def control_motor(direction_motor1, direction_motor2, speed_motor1, speed_motor2):
    if direction_motor1 == 1:
        GPIO.output(motor1_in1, GPIO.HIGH)
        GPIO.output(motor1_in2, GPIO.LOW)
    else:
        GPIO.output(motor1_in1, GPIO.LOW)
        GPIO.output(motor1_in2, GPIO.HIGH)

    if direction_motor2 == 1:
        GPIO.output(motor2_in1, GPIO.HIGH)
        GPIO.output(motor2_in2, GPIO.LOW)
    else:
        GPIO.output(motor2_in1, GPIO.LOW)
        GPIO.output(motor2_in2, GPIO.HIGH)

    pwm_motor1.ChangeDutyCycle(speed_motor1)
    pwm_motor2.ChangeDutyCycle(speed_motor2)

# Function to calculate the time to move 3 feet
def move_distance(distance):
    wheel_diameter = 0.062  # Wheel diameter in meters (62 mm)
    wheel_circumference = 3.1416 * wheel_diameter  # Circumference in meters
    motor1_rpm = 135  # Motor 1 RPM at 6V
    motor2_rpm = 126 # Motor 2 RPM at 6V

    meters_per_minute1 = (motor1_rpm * wheel_circumference)/60  # Speed in meters per minute
    meters_per_minute2 = (motor2_rpm * wheel_circumference)/60  # Speed in meters per minute


    # Convert 3 feet to meters (1 foot = 0.3048 meters)
    distance_meters = distance * 0.3048
    
    # Calculate the time required to move the given distance (in minutes)
    time_to_move = distance_meters / min(meters_per_minute1, meters_per_minute2)  # Time in seconds

    print(f"Time to move {distance} feet: {time_to_move + 0.6} seconds")
    
    # Move forward for the calculated time
    move_forward(time_to_move)

# Function to move the car forward for a given time
def move_forward(time_to_move):
    direction_motor1 = 1
    direction_motor2 = 1
    speed_motor1 = 100  # Speed percentage (adjust as needed)
    speed_motor2 = 77.5  # Speed percentage (adjust as needed)

    control_motor(direction_motor1, direction_motor2, speed_motor1, speed_motor2)

    time.sleep(time_to_move + 0.6)  # Run both motors together for the minimum time

    # Stop both motors together
    control_motor(0, 0, 0, 0)

# Main loop
try:
    time.sleep(3)
    GPIO.output(20, GPIO.HIGH)  # Set LED to High
    move_distance(3)  # Move forward 3 feet
finally:
    pwm_motor1.stop()
    pwm_motor2.stop()
    GPIO.cleanup()  # Clean up the GPIO pins
