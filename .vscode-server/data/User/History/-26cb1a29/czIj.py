# blink.py
# Import necessary libraries
import time
import RPi.GPIO as GPIO

# Set GPIO mode
GPIO.setmode(GPIO.BCM)  # Set for GPIO numbering, not pin numbers

# Set GPIO pin 13 as output
GPIO.setup(16, GPIO.OUT)

# Blink the LED 10 times
i = 0
while i < 10:
    GPIO.output(16, GPIO.HIGH)  # Turn the LED on
    time.sleep(0.5)             # Wait for 0.5 seconds
    GPIO.output(16, GPIO.LOW)   # Turn the LED off
    time.sleep(0.5)             # Wait for 0.5 seconds
    i += 1

# Cleanup GPIO settings
GPIO.cleanup()