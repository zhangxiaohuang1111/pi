import RPi.GPIO as GPIO
import time
import sys

# Setup GPIO pin for the LED
LED_PIN = 26  # You can change this to the GPIO pin connected to your LED

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set LED_PIN as output
GPIO.setup(LED_PIN, GPIO.OUT)

# Default blink frequency in Hz
DEFAULT_FREQUENCY = 1  # 1 Hz (1 blink per second)

# Function to blink the LED
def blink_led(frequency):
    """Blink the LED at the given frequency (in Hz)."""
    period = 1.0 / frequency  # Calculate period from frequency
    half_period = period / 2   # Half period for ON and OFF time

    for _ in range(10):  # Blink the LED 10 times
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
        time.sleep(half_period)
        GPIO.output(LED_PIN, GPIO.LOW)   # Turn LED off
        time.sleep(half_period)

# Main function to control the LED blink
if __name__ == "__main__":
    try:
        # If a frequency argument is passed, use it; otherwise, use the default
        if len(sys.argv) > 1:
            frequency = float(sys.argv[1])
        else:
            frequency = DEFAULT_FREQUENCY

        print(f"Blinking LED at {frequency} Hz.")
        blink_led(frequency)

    except KeyboardInterrupt:
        print("Program interrupted.")

    finally:
        # Clean up GPIO setup
        GPIO.cleanup()