# Import Statements
import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
# Set Warnings to False
GPIO.setwarnings(False)

# Define GPIO pins connected to the L293D motor driver
motor1_in1 = 20
motor1_in2 = 21
motor2_in1 = 18
motor2_in2 = 19 
enable_motor1 = 13  # Enable pin for motor 1 (PWM)
enable_motor2 = 12  # Enable pin for motor 2 (PWM)

# Setup the GPIO pins
GPIO.setup(motor1_in1, GPIO.OUT)
GPIO.setup(motor1_in2, GPIO.OUT)
GPIO.setup(motor2_in1, GPIO.OUT)
GPIO.setup(motor2_in2, GPIO.OUT)
GPIO.setup(enable_motor1, GPIO.OUT) # Controls the speed of the motor
GPIO.setup(enable_motor2, GPIO.OUT) # Controls the speed of the motor

# Initialize PWM for motor speed control
pwm_motor1 = GPIO.PWM(enable_motor1, 100)  # 100 Hz frequency for PWM
pwm_motor2 = GPIO.PWM(enable_motor2, 100)
pwm_motor1.start(0)  # Start with 0% duty cycle (motor off)
pwm_motor2.start(0)  # Start with 0% duty cycle (motor off)

# Transfer function constants for each motor
K1 = 41.044  # Gain for motor 1
K2 = 42.24  # Gain for motor 2
tau = 0.000125  # Time constant for both motors
dt = 0.1  # Time step (seconds)

# Initialize motor speeds (RPM)
rpm_motor1 = 0
rpm_motor2 = 0

# Discrete-time model of the transfer function (1st order)
def update_motor_speed(voltage, motor_num):
    """Update motor speed using the transfer function (discrete-time model)"""
    if motor_num == 1:
        K = K1
    else:
        K = K2

    # Discrete-time update of the transfer function
    motor_speed = (K / tau) * voltage * dt + rpm_motor1  # Using same logic for both motors
    return motor_speed

# Function to control motor direction and speed
def control_motor(direction_motor1, direction_motor2, speed_motor1, speed_motor2):
    # Motor 1 direction
    if direction_motor1 == 1:
        # Forward
        GPIO.output(motor1_in1, GPIO.HIGH)
        GPIO.output(motor1_in2, GPIO.LOW)
    else:
        # Backward
        GPIO.output(motor1_in1, GPIO.LOW)
        GPIO.output(motor1_in2, GPIO.HIGH)

    # Motor 2 direction
    if direction_motor2 == 1:
        # Forward
        GPIO.output(motor2_in1, GPIO.HIGH)
        GPIO.output(motor2_in2, GPIO.LOW)
    else:
        # Backward
        GPIO.output(motor2_in1, GPIO.LOW)
        GPIO.output(motor2_in2, GPIO.HIGH)

    # Set PWM duty cycle to control speed
    pwm_motor1.ChangeDutyCycle(speed_motor1)
    pwm_motor2.ChangeDutyCycle(speed_motor2)

# Main loop
try:
    while True:
        # Example desired voltage for both motors (same control voltage for both)
        control_voltage = 6  # Example control voltage in volts (adjust as needed)

        # Simulate the motor speed using the transfer function for both motors
        rpm_motor1 = update_motor_speed(control_voltage, 1) # Motor 1
        rpm_motor2 = update_motor_speed(control_voltage, 2) # Motor 2

        # Convert motor speeds to PWM duty cycle (0-100 scale)
        speed_motor1 = min(max((rpm_motor1 / 300) * 100, 0), 100)
        speed_motor2 = min(max((rpm_motor2 / 300) * 100, 0), 100)

        # Assume forward direction for both motors
        direction_motor1 = 1
        direction_motor2 = 1

        # Control both motors to run at the same speed
        control_motor(direction_motor1, direction_motor2, speed_motor1, speed_motor2)

        time.sleep(dt)  # Update every 100 ms

except KeyboardInterrupt:
    pwm_motor1.stop() # End
    pwm_motor2.stop() # End
    GPIO.cleanup() # Clears the pins
    

