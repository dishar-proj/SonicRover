# Effective One
import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)

led_pin = 18
switch_pin = 25

GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Debounce parameters
last_time = 0
debounce_delay = .05  # 50ms debounce delay

# Callback function for switch press
def toggle_led(channel):
    global last_time
    current_time = time.time()
    if current_time - last_time > debounce_delay:  # Check debounce delay
        GPIO.output(led_pin, not GPIO.input(led_pin))  # Toggle LED
        last_time = current_time

# Add event detection with a callback
GPIO.add_event_detect(switch_pin, GPIO.FALLING, callback=toggle_led, bouncetime=50)

try:
    while True:
        time.sleep(.1)  # Main program loop
except KeyboardInterrupt:
    GPIO.cleanup()
