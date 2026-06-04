import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(19, GPIO.OUT)
GPIO.output(19, GPIO.LOW)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)

GPIO.setup(18, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

GPIO.output(18, GPIO.HIGH) 
GPIO.output(20, GPIO.HIGH)

# Pins connected to the motors
motorPin1 = 6
motorPin2 = 26
pulsesPerRev = 20

# Shared pulse counters
pulseCount1 = 0
pulseCount2 = 0

# Callback functions to count pulses
def count_pulse1(channel):
    global pulseCount1  # Declare the global variable
    pulseCount1 += 1

def count_pulse2(channel):
    global pulseCount2  # Declare the global variable
    pulseCount2 += 1

# Setup GPIO for encoders
GPIO.setup(motorPin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(motorPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(motorPin1, GPIO.RISING, callback=count_pulse1)
GPIO.add_event_detect(motorPin2, GPIO.RISING, callback=count_pulse2)

try:
    while True:
        # Measure RPM every second
        time.sleep(1)

        # Calculate RPM for motor 1
        rpm1 = (pulseCount1 / pulsesPerRev) * 60
        print(f"Motor 1 RPM: {rpm1:.2f}")
        pulseCount1 = 0  # Reset the count for the next interval

        # Calculate RPM for motor 2
        rpm2 = (pulseCount2 / pulsesPerRev) * 60
        print(f"Motor 2 RPM: {rpm2:.2f}")
        pulseCount2 = 0  # Reset the count for the next interval

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
