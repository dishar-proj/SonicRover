# Group 16
# Author: Emerson Hall

# import statements
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

# LED Output Pins
led_bit3 = 14  # Red LED
led_bit2 = 24  # Yellow LED
led_bit1 = 25  # Blue LED
led_bit0 = 23  # Green LED

# Set up DIP switch pins as input
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)

# Set up LED pins as output
GPIO.setup(14, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

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

# Move forward for a given time
def move_forward(time_to_move):
    control_motor(1, 1, 100, 77.5)  # Move both motors forward
    time.sleep(time_to_move + 0.8)
    control_motor(0, 0, 0, 0)  # Stop motors
    time.sleep(0.1)

# Rotate 90 degrees in place (adjust timing as needed)
def turn_right():
    control_motor(1, 0, 100, 0)  # Motor 1 forward, Motor 2 stopped
    time.sleep(0.8)  # Adjust this time to achieve a 90-degree turn
    control_motor(0, 0, 0, 0)  # Stop motors
    time.sleep(0.1)

# Rotate for figure 8 
def turn_right8():
    control_motor(1, 1, 100, 30)  # Motor 1 forward, Motor 2 slow
    time.sleep(3.9)  # Adjust this time to achieve an arch turn
    control_motor(0, 0, 0, 0)  # Stop motors

# Make a left turn (~120 degrees for a curved path)
def turn_left8():
    control_motor(1, 1, 40, 100)  # Motor 1 slow, Motor 2 forward
    time.sleep(3.1)  # Adjust this time for a smoother left arch turn
    control_motor(0, 0, 0, 0)  # Stop motors
    time.sleep(1)

# Function to calculate the time to move a certain distance
def move_distance(feet):
    wheel_diameter = 0.062  # Wheel diameter in meters (62 mm)
    wheel_circumference = 3.1416 * wheel_diameter  # Circumference in meters
    motor1_rpm = 135  # Motor 1 RPM at 5V
    motor2_rpm = 126  # Motor 2 RPM at 5V
    meters_per_minute1 = (motor1_rpm * wheel_circumference) / 60
    meters_per_minute2 = (motor2_rpm * wheel_circumference) / 60
    distance_meters = feet * 0.3048  # Convert feet to meters
    time_to_move = distance_meters / min(meters_per_minute1, meters_per_minute2)
    move_forward(time_to_move)

# Move in a square pattern
def move_square():
    for _ in range(4):
        move_distance(3)  # Move forward 3 feet
        time.sleep(1)
        turn_right()  # Turn 90 degrees
        time.sleep(1)
        move_distance(3)  # Move forward 3 feet
        time.sleep(1)
        turn_right()  # Turn 90 degrees
        time.sleep(1)

# Move in a figure-8 pattern
def move_figure_8():
    for _ in range(2):  # Complete the figure-8 twice
        move_distance(3)  # Move forward 3 feet
        turn_right8()  # Turn right
        move_distance(3)  # Move forward 3 feet
        turn_left8()  # Turn right

# Read DIP Switch
def read_dip():
    return (GPIO.input(4) << 3) | (GPIO.input(17) << 2) | (GPIO.input(27) << 1) | GPIO.input(22)
    
# Main loop
try:
    last_dip_value = 0b0000 # Stores last know DIP switch state
    action_done = False # FLag to track action
    
    # While loop for figures
    while True:
        dip_value = read_dip()

        # Resets flag with all pins 0
        if dip_value == 0b0000:
            control_motor(0,0,0,0)
            action_done = False # Reset the flag when DIP is reset
            GPIO.output(led_bit3, GPIO.LOW)
            GPIO.output(led_bit2, GPIO.LOW)
            GPIO.output(led_bit1, GPIO.LOW)
            GPIO.output(led_bit0, GPIO.LOW)

        # If flag is false, it continues
        if not action_done:
            if dip_value == 0b1111:  # Debug
                print("DIP switch setting: 1111 (Debug)")
                GPIO.output(led_bit3, GPIO.HIGH)
                GPIO.output(led_bit2, GPIO.HIGH)
                GPIO.output(led_bit1, GPIO.HIGH)
                GPIO.output(led_bit0, GPIO.HIGH)
                time.sleep(3)
                # Add debug behavior here if needed
            elif dip_value == 0b1110:  # Square
                print("DIP switch setting: 1110 (Square)")
                GPIO.output(led_bit3, GPIO.HIGH)
                GPIO.output(led_bit2, GPIO.HIGH)
                GPIO.output(led_bit1, GPIO.HIGH)
                GPIO.output(led_bit0, GPIO.LOW)
                action_done = True
                time.sleep(3)
                move_square()
            elif dip_value == 0b1101:  # Figure-8
                print("DIP switch setting: 1101 (Figure-8)")
                GPIO.output(led_bit3, GPIO.HIGH)
                GPIO.output(led_bit2, GPIO.HIGH)
                GPIO.output(led_bit1, GPIO.LOW)
                GPIO.output(led_bit0, GPIO.HIGH)
                action_done = True
                time.sleep(3)
                move_figure_8()
            elif dip_value == 0b1100:  # Straight
                print("DIP switch setting: 1100 (Straight)")
                GPIO.output(led_bit3, GPIO.HIGH)
                GPIO.output(led_bit2, GPIO.HIGH)
                GPIO.output(led_bit1, GPIO.LOW)
                GPIO.output(led_bit0, GPIO.LOW)
                action_done = True
                time.sleep(3)
                move_distance(3)  # Move forward 3 feet
            elif dip_value == 0b1001:  # Multiple
                print("DIP switch setting: 1001 (Multiple)")
                GPIO.output(led_bit3, GPIO.HIGH)
                GPIO.output(led_bit2, GPIO.LOW)
                GPIO.output(led_bit1, GPIO.LOW)
                GPIO.output(led_bit0, GPIO.HIGH)
                # Add multiple behavior here if needed
            elif dip_value == 0b1000:  # Single
                print("DIP switch setting: 1000 (Single)")
                GPIO.output(led_bit3, GPIO.HIGH)
                GPIO.output(led_bit2, GPIO.LOW)
                GPIO.output(led_bit1, GPIO.LOW)
                GPIO.output(led_bit0, GPIO.LOW)
                # Add single behavior here if needed
            else:
                control_motor(0,0,0,0)
                GPIO.output(led_bit3, GPIO.LOW)
                GPIO.output(led_bit2, GPIO.LOW)
                GPIO.output(led_bit1, GPIO.LOW)
                GPIO.output(led_bit0, GPIO.LOW)
                print(f"DIP switch setting: {dip_value:04b} (No action)")

        time.sleep(1)  # Delay between checks
finally:
    pwm_motor1.stop()
    pwm_motor2.stop()
    GPIO.cleanup()  # Clean up the GPIO pins
