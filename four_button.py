import RPi.GPIO as GPIO
import time

# Define GPIO pins for the four buttons based on the piTFT schematic
BUTTON_PINS = {
    17: "Button 17",  # Example pin numbers, replace with the actual pins from the schematic
    22: "Button 22",
    23: "Button 23",
    27: "Button 27"   # Assuming this is an "edge" button for the quit function
}

# Callback function that gets called when a button is pressed
def button_callback(channel):
    if channel in BUTTON_PINS:
        print(f"{BUTTON_PINS[channel]} has been pressed")
        # Check if it's the edge button (e.g., GPIO 27) and quit the program
        if channel == 27:  # Replace 27 with the actual edge button pin if necessary
            print(f"{BUTTON_PINS[channel]} has been pressed. Exiting program...")
            GPIO.cleanup()  # Clean up before exiting
            exit(0)

def main():
    # Set GPIO numbering to Broadcom (BCM)
    GPIO.setmode(GPIO.BCM)

    # Set up each button pin as an input with an internal pull-up resistor
    for pin in BUTTON_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Add an event listener for each button press (falling edge detection)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

    print(f"Monitoring buttons: {', '.join([str(pin) for pin in BUTTON_PINS])}.")
    print("Press any button to see a message. Press the edge button to quit.")

    try:
        # Keep the script running to monitor button presses
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Clean up GPIO settings
        GPIO.cleanup()

if __name__ == "__main__":
    main()
