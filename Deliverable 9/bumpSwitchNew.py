#top of code
bump_switch_pin = 23 #already in code, just past the stopped line after
stopped = False

def is_bump_switch_pressed(): #replace the code in the method
  while True:
          if GPIO.input(bump_switch_pin) == GPIO.LOW:  # Button is pressed
              stopped = True  # Freeze
        
          if stopped:
              stop_motor()
        
          time.sleep(0.1)  # Small delay to prevent excessive CPU usage
