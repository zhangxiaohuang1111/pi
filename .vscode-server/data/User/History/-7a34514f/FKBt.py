import os
import RPi.GPIO as GPIO
import time

FIFO_PATH = "/home/pi/video_fifo"  # Path to the FIFO file that mplayer monitors

BUTTON_PINS = {  # GPIO pins for each button
    '30s_forward': 13,
    'pause': 17,
    'fast_forward': 22,
    'rewind': 23,
    '30s_rewind': 26,
    'quit': 27
}

COMMANDS = {  # Corresponding mplayer commands for each button
    '30s_forward': "seek 30",
    'pause': "pause",
    'fast_forward': "seek 10",
    'rewind': "seek -10",
    '30s_rewind': "seek -30",
    'quit': "quit"
}

def send_command(command):
    """Send command to mplayer via FIFO."""
    if os.path.exists(FIFO_PATH):
        with open(FIFO_PATH, 'w') as fifo:
            fifo.write(command + '\n')
    else:
        print("FIFO file not found.")

def button_callback(channel):
    """Handle button press, debug interrupt trigger, and send corresponding command to mplayer."""
    button = next(key for key, pin in BUTTON_PINS.items() if pin == channel)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # Get current time for debugging
    print(f"[{timestamp}] Interrupt triggered on GPIO {channel} ({button} button pressed)")

    # Send the corresponding command to mplayer
    send_command(COMMANDS[button])

    # If the quit button is pressed, clean up and exit
    if button == 'quit':
        GPIO.cleanup()
        print(f"[{timestamp}] Quit button pressed, exiting program.")
        exit()

def main():
    GPIO.setmode(GPIO.BCM)  # Set GPIO mode to BCM numbering
    print("Setting up GPIO pins...")

    # Setup each button pin with pull-up resistors and interrupt detection
    for button, pin in BUTTON_PINS.items():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_callback, bouncetime=300)
        print(f"Interrupt set for {button} on GPIO {pin}")

    print("Ready for button presses. Press Ctrl+C to exit.")
    
    try:
        while True:  # Keep the script running for debugging
            time.sleep(1)  # Sleep to reduce CPU usage and keep the program alive
    except KeyboardInterrupt:
        print("\nExiting due to keyboard interrupt...")
    finally:
        GPIO.cleanup()
        print("GPIO cleanup completed.")

if __name__ == "__main__":
    main()