import RPi.GPIO as GPIO
import time

# Define the GPIO pins for the buttons (replace with actual pin numbers)
BUTTON_PINS = [17, 22, 23, 27]  # Example GPIO pins, adjust based on your piTFT schematic

def button_callback(channel):
    """Callback function to handle button presses."""
    print(f"Button {channel} has been pressed")
    
    # If the button on the edge (e.g., GPIO 27) is pressed, quit the program
    if channel == 27:  # Replace with the actual pin number of the edge button
        print(f"Button {channel} has been pressed, quitting program.")
        GPIO.cleanup()
        exit()

def main():
    # Set GPIO numbering to Broadcom (BCM)
    GPIO.setmode(GPIO.BCM)
    
    # Set up each button pin as input with pull-up resistor and attach callback
    for pin in BUTTON_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_callback, bouncetime=300)
    
    print("Monitoring all buttons. Press any button to see a message.")

    try:
        # Keep the script running to monitor button presses
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
