METHOD single_sound_behavior:
  GLOBAL variable STOPPED
  WHILE STOPPED is FALSE:
      adc_value = read_adc()

      IF adc_value == 000:
          PRINT("ADC: Car is Turning Left at Normal Speed")
          SET control_motor(1, 0, 80, 0) #This makes the car turn to left at a normal speed.
      ELSE IF adc_value == 001:
          PRINT("ADC: Car is Turning Left at Slower Speed")
          SET control_motor(1, 0, 72.5, 0) #Turn left slower
      ELSE IF adc_value == 011:
          PRINT("ADC: Car is Slowing Down Even More but Still Turning Left")
          SET control_motor(1, 0, 60, 0) #Turns left even slower
      ELSE IF adc_value == 111:
          PRINT("ADC: Car is Stopping to Confirm")
          SET control_motor(0, 0, 0, 0) #Stop car
          WAIT for 0.5 seconds #time sleeps

          IF read_adc() == 111:
              PRINT("ADC: Confirmed. Moving Forward")

              WHILE is_bump_switch_pressed() is FALSE:
                  SET control_motor(1, 1, 100, 77.5) #Moves forward
              PRINT("Bump Switch Activated! Stopping.")
              SET STOPPED to TRUE
