import RPi.GPIO as GPIO
import time

# Define the GPIO pin for the button (replace XX with the actual pin number from the schematic)
BUTTON_PIN = 17  # Example: 17, 22, 23, or 27 based on your piTFT schematic

def button_callback(channel):
    """Callback function that gets called when the button is pressed."""
    print(f"Button {channel} has been pressed")

def main():
    # Set GPIO numbering to Broadcom (BCM)
    GPIO.setmode(GPIO.BCM)
    
    # Set up the button pin as an input with an internal pull-up resistor
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Add an event listener for the button press (falling edge detection)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)
    
    print(f"Monitoring button on GPIO {BUTTON_PIN}. Press the button to see a message.")
    
    try:
        # Keep the script running to monitor the button press
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Clean up GPIO settings
        GPIO.cleanup()

if __name__ == "__main__":
    main()
