# Group 16
# Authors: Emerson Hall and Disha Rachur and Navi Jha

# import statements
import RPi.GPIO as GPIO
import time

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

# ADC
comp1_output = 24 # MSB
comp2_output = 25  # Middle bit
comp3_output = 8  # LSB

# Bump Switch
bump_switch_pin = 23  # Bump switch pin (adjust as needed)

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

# Function to control motors (direction and speed)
def control_motor(direction_motor1, direction_motor2, speed_motor1, speed_motor2):
    GPIO.output(motor1_in1, GPIO.HIGH if direction_motor1 == 1 else GPIO.LOW)
    GPIO.output(motor1_in2, GPIO.LOW if direction_motor1 == 1 else GPIO.HIGH)
    GPIO.output(motor2_in1, GPIO.HIGH if direction_motor2 == 1 else GPIO.LOW)
    GPIO.output(motor2_in2, GPIO.LOW if direction_motor2 == 1 else GPIO.HIGH)
    pwm_motor1.ChangeDutyCycle(speed_motor1)
    pwm_motor2.ChangeDutyCycle(speed_motor2)

# Read states of comparators and convert to 3-bit ADC value
def read_adc():
    comp1_state = GPIO.input(comp1_output)  # MSB (bit 2)
    comp2_state = GPIO.input(comp2_output)  # Middle bit (bit 1)
    comp3_state = GPIO.input(comp3_output)  # LSB (bit 0)
    
    # Combine the bits into a 3-bit number (binary to integer)
    adc_value = (comp1_state << 2) | (comp2_state << 1) | comp3_state
    
    return adc_value

# Read bump switch state
def is_bump_switch_pressed():
    return GPIO.input(bump_switch_pin) == GPIO.LOW  # LOW when pressed

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

# Single Sound Behavior - When ADC detects a value of 111 (sound detected)
def single_sound_behavior():
    while True:
        # Read ADC
        adc_value = read_adc()
        
        # Read ADC and turn left
        if adc_value == 0b000:
            print("ADC: {} - Turning Left (Normal Speed)".format(bin(adc_value)))
            control_motor(1, 0, 90, 0)  # Left turn (normal speed)
        
        # Read the ADC and turn slower
        elif adc_value == 0b001:
            print("ADC: {} - Turning Left (Slower)".format(bin(adc_value)))
            control_motor(1, 0, 80, 0)  # Slower left turn
        
        # Read the ADC and turn slowest
        elif adc_value == 0b011:
            print("ADC: {} - Slowing Down Even More but Still Turning Left".format(bin(adc_value)))
            control_motor(1, 0, 70, 0)  # Even slower left turn
        
        # Read the ADC value to detect the sound
        elif adc_value == 0b111:
            print("ADC: {} - Stopping to Confirm".format(bin(adc_value)))
            control_motor(0, 0, 0, 0)  # Stop
            time.sleep(0.5)  # Small delay before rechecking
            
            # Reread the ADC to confirm
            if read_adc() == 0b111:
                print("ADC: {} - Confirmed. Moving Forward".format(bin(adc_value)))
                while not is_bump_switch_pressed(): # Detect the bump switch
                    control_motor(1, 1, 100, 90)
                    time.sleep(0.1)
                print("Bump switch activated! Stopping.")
                stopped = True         

# Read DIP Switch
def read_dip():
    return (GPIO.input(4) << 3) | (GPIO.input(17) << 2) | (GPIO.input(27) << 1) | GPIO.input(22)
    
# Main loop
try:
    last_dip_value = 0b0000 # Stores last know DIP switch state
    action_done = False # Flag to track action
    stopped = False # Bump Switch
    
    # While loop for figures
    while True:
        dip_value = read_dip()

        # Resets flag with all pins 0
        if dip_value == 0b0000:
            control_motor(0,0,0,0)
            action_done = False # Reset the flag when DIP is reset
            stopped = False # Reset bump switch
        # If flag is false, it continues
        if stopped: 
            control_motor(0,0,0,0)
            print("Bump switch was pressed. Reset DIP switch to resume.")
        else:
            if not action_done:
                if dip_value == 0b1111:  # Debug
                    print("DIP switch setting: 1111 (Debug)")
                    time.sleep(3)
                    # Add debug behavior here if needed
                elif dip_value == 0b1110:  # Square
                    print("DIP switch setting: 1110 (Square)")
                    action_done = True
                    time.sleep(3)
                    move_square()
                elif dip_value == 0b1101:  # Figure-8
                    print("DIP switch setting: 1101 (Figure-8)")
                    action_done = True
                    time.sleep(3)
                    move_figure_8()
                elif dip_value == 0b1100:  # Straight
                    print("DIP switch setting: 1100 (Straight)")
                    action_done = True
                    time.sleep(3)
                    move_distance(3.2)  # Move forward 3 feet
                elif dip_value == 0b1001:  # Multiple
                    print("DIP switch setting: 1001 (Multiple)")
                    # Add multiple behavior here if needed
                elif dip_value == 0b1000:  # Single
                    action_done = True
                    print("DIP switch setting: 1000 (Single)")
                    time.sleep(2)   
                    single_sound_behavior()
                    time.sleep(0.1)  # Small delay to avoid high CPU usage
                else:
                    control_motor(0,0,0,0)
                    print(f"DIP switch setting: {dip_value:04b} (No action)")

            time.sleep(1)  # Delay between checks
finally:
    pwm_motor1.stop()
    pwm_motor2.stop()
    GPIO.cleanup()  # Clean up the GPIO pins
