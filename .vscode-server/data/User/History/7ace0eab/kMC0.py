import os
import RPi.GPIO as GPIO
import time

# Path to the FIFO file that mplayer is monitoring
FIFO_PATH = "/home/pi/video_fifo"  # Adjust to your actual FIFO file path

# Define GPIO pins for the buttons (replace with actual pin numbers)
BUTTON_PINS = {
    '30s_forward': 13,  # Fast forward 30 seconds GPIO pin
    'pause': 17,       # Pause button GPIO pin
    'fast_forward': 22,  # Fast forward 10 seconds GPIO pin
    'rewind': 23,      # Rewind 10 seconds GPIO pin
    '30s_rewind': 26,  # Rewind 30 seconds GPIO pin
    'quit': 27         # Quit mplayer GPIO pin
}

def send_command_to_mplayer(command):
    """Send the command to the mplayer instance via the FIFO."""
    if os.path.exists(FIFO_PATH):
        with open(FIFO_PATH, 'w') as fifo:
            fifo.write(command + '\n')
    else:
        print(f"FIFO file {FIFO_PATH} not found.")

def main():
    # Set GPIO numbering to Broadcom (BCM)
    GPIO.setmode(GPIO.BCM)

    # Set up each button pin as input with pull-up resistors
    for pin in BUTTON_PINS.values():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        # Keep polling the button states in a loop
        while True:
            if GPIO.input(BUTTON_PINS['pause']) == GPIO.LOW:
                print("Pause button pressed")
                send_command_to_mplayer("pause")
                time.sleep(0.3)  # Debounce delay

            if GPIO.input(BUTTON_PINS['30s_forward']) == GPIO.LOW:
                print("Fast forward 30 seconds button pressed")
                send_command_to_mplayer("seek 30")
                time.sleep(0.3)

            if GPIO.input(BUTTON_PINS['30s_rewind']) == GPIO.LOW:
                print("Rewind 30 seconds button pressed")
                send_command_to_mplayer("seek -30")
                time.sleep(0.3)

            if GPIO.input(BUTTON_PINS['fast_forward']) == GPIO.LOW:
                print("Fast forward button pressed")
                send_command_to_mplayer("seek 10")
                time.sleep(0.3)

            if GPIO.input(BUTTON_PINS['rewind']) == GPIO.LOW:
                print("Rewind button pressed")
                send_command_to_mplayer("seek -10")
                time.sleep(0.3)

            if GPIO.input(BUTTON_PINS['quit']) == GPIO.LOW:
                print("Quit button pressed")
                send_command_to_mplayer("quit")
                break

            time.sleep(0.1)  # Small delay to reduce CPU usage

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()