def specific_move():
  current speed = 100
  while True:
      adc_value = read_adc()

      if adc_value == 0b11:
          print("Turn")
          turn_right()
          current_speed = 100
      elif adc_value == 0b01:
            print("Slower movement")
            control_motor(1,1,45,45)
      else:
            print("waiting")
            control_motor(0,0,0,0)

time.sleep(3)

#call this  method in main file if it functions. 
