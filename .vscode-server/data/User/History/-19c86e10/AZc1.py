# blink_pwm.py
# Import necessary libraries
import time
import RPi.GPIO as GPIO
GPIO.cleanup()
# Set GPIO mode
GPIO.setmode(GPIO.BCM)  # Set for GPIO numbering, not pin numbers

# Set GPIO pin 5 as output
GPIO.setup(16, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
# Set PWM parameters
freq = 1  # Set frequency to 1 Hz
duty_cycle = 50  # Set duty cycle to 50% (LED on for half the time)

# Create a PWM instance
pwm = GPIO.PWM(16, freq)
pwm.start(duty_cycle)

try:
    while True:
        # Ask user for a new frequency input
        user_input = input("Enter new frequency (or 0 to quit): ")
        new_freq = int(user_input)
        
        if new_freq == 0:
            print("Exiting program...")
            break
        
        # Change frequency of PWM
        pwm.ChangeFrequency(new_freq)
        print(f"Frequency set to {new_freq} Hz")

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    # Stop PWM and cleanup GPIO settings
    pwm.stop()
    GPIO.cleanup()