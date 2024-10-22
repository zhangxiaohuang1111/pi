import RPi.GPIO as GPIO
import time

# GPIO pin setup for LED
LED_PIN = 26  # Set to the GPIO pin you connected the LED to
BLINK_FREQUENCY = 1  # Default blink frequency is 1 Hz

# Setup GPIO mode and disable warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set LED_PIN as output
GPIO.setup(LED_PIN, GPIO.OUT)

# Function to blink the LED with a given frequency
def blink_led(frequency):
    """Blink LED at a given frequency (in Hz) with a 50% duty cycle."""
    period = 1.0 / frequency  # Calculate period from frequency
    half_period = period / 2   # Half period for ON and OFF time

    for _ in range(10):  # Blink the LED 10 times
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
        time.sleep(half_period)          # Sleep for half the period
        GPIO.output(LED_PIN, GPIO.LOW)   # Turn LED off
        time.sleep(half_period)          # Sleep for the remaining half

# Main function to read frequency and blink LED
if __name__ == "__main__":
    try:
        print("Starting blink.py. Type frequency in Hz (or 0 to quit):")
        while True:
            user_input = input("Enter blink frequency (Hz): ")
            
            try:
                frequency = int(user_input)
            except ValueError:
                print("Please enter a valid integer.")
                continue
            
            # Exit if user inputs 0
            if frequency == 0:
                print("Exiting program.")
                break

            if frequency > 0:
                print(f"Blinking LED at {frequency} Hz")
                blink_led(frequency)
            else:
                print("Invalid frequency. Enter a positive integer or 0 to quit.")

    except KeyboardInterrupt:
        print("Program interrupted.")

    finally:
        # Clean up GPIO settings
        GPIO.cleanup()